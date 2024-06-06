# views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem, Order, Address, Payment
from .serializers import OrderItemSerializer, OrderSerializer, AddressSerializer
from .helpers import get_or_create_session_cart
from ..product.models import Product, Image
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


class AddToCartView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create the order
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=request.user, status='open')
        else:
            order = get_or_create_session_cart(request)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        total_price = product.price * quantity

        # Create the order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            total_price=total_price,
        )

        serializer = self.get_serializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OrderView(View):
    def get(self, request):
        total_items, total_price, products, cart_order = self.get_cart_details(request)
        product_images = self.get_images_for_products(products)

        return render(request, 'orders.html', {
            'cart_orders': [cart_order] if cart_order else [],
            'products': products,
            'total_items': total_items,
            'total_price': total_price,
            'images': product_images
        })

    def get_cart_details(self, request):
        total_items = 0
        total_price = 0
        products = []

        if request.user.is_authenticated:
            cart_order, products = self.handle_authenticated_user_cart(request)
        else:
            cart_order = self.get_or_create_session_cart(request)
            products = OrderItem.objects.filter(order=cart_order)

        for product in products:
            total_items += product.quantity
            total_price += product.quantity * product.product.price
        cart_order.total_amount = total_price
        cart_order.save()

        return total_items, total_price, products, cart_order

    def handle_authenticated_user_cart(self, request):
        cart_orders = Order.objects.filter(customer=request.user, status='open')
        if cart_orders.exists():
            cart_order = cart_orders.first()
            session_cart_order_id = request.session.get('cart_order')
            if session_cart_order_id:
                try:
                    session_cart_order = Order.objects.get(id=session_cart_order_id, status='open')
                    if session_cart_order and session_cart_order != cart_order:
                        self.merge_carts(cart_order, session_cart_order)
                        request.session['cart_order'] = cart_order.id
                except ObjectDoesNotExist:
                    logger.warning(f'Session cart order with id {session_cart_order_id} does not exist.')
            products = OrderItem.objects.filter(order=cart_order)
        else:
            cart_order = self.get_or_create_session_cart(request)
            products = OrderItem.objects.filter(order=cart_order)

        return cart_order, products

    def merge_carts(self, user_cart, session_cart):
        try:
            with transaction.atomic():
                for item in OrderItem.objects.select_for_update().filter(order=session_cart):
                    existing_item = OrderItem.objects.filter(order=user_cart, product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.total_price += item.total_price
                        existing_item.save()
                    else:
                        OrderItem.objects.create(
                            order=user_cart,
                            product=item.product,
                            quantity=item.quantity,
                            total_price=item.total_price
                        )
                session_cart.delete()
        except Exception as e:
            logger.error(f'Error merging carts: {e}')
            raise

    def get_or_create_session_cart(self, request):
        session_cart_order_id = request.session.get('cart_order')
        if session_cart_order_id:
            try:
                return Order.objects.get(id=session_cart_order_id, status='open')
            except ObjectDoesNotExist:
                logger.warning(f'Session cart order with id {session_cart_order_id} does not exist.')
        session_cart_order = Order.objects.create(status='open')
        request.session['cart_order'] = session_cart_order.id
        return session_cart_order

    def get_images_for_products(self, products):
        product_ids = [item.product.id for item in products]
        images = Image.objects.filter(product_id__in=product_ids)

        product_images = {}
        for image in images:
            if image.product_id not in product_images:
                product_images[image.product_id] = image

        return product_images


class OrderItemCreate(generics.CreateAPIView):
    serializer_class = OrderItemSerializer


class OrderAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(customer=self.request.user)
        return Order.objects.none()


class AddressAPIView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Address.objects.filter(customer=self.request.user)
        return Address.objects.none()


class CheckOutView(LoginRequiredMixin, View):
    def get(self, request):
        cart_id = request.session.get('cart_id')
        user_order, created = Order.objects.get_or_create(customer=request.user, status='open')

        if cart_id:
            try:
                cart_order = Order.objects.get(id=cart_id, status='open')
                self._merge_cart_order_items(cart_order, user_order)
                cart_order.delete()
                del request.session['cart_id']
            except Order.DoesNotExist:
                pass

        return redirect('payment-initiate', order_id=user_order.id)

    def _merge_cart_order_items(self, cart_order, user_order):
        for item in OrderItem.objects.filter(order=cart_order):
            item.order = user_order
            item.save()


class PaymentInitiateView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user, status='open')
        return render(request, 'payment_initiate.html', {'order': order})

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id,customer=request.user, status='open')
        payment_type = request.POST.get('payment_type')
        transaction_id = request.POST.get('transaction_id')
        amount = order.total_amount

        payment = Payment.objects.create(
            order=order,
            payment_type=payment_type,
            transaction_id=transaction_id,
            amount=amount
        )

        order.status = 'pending'
        order.save()

        return redirect('payment-success', payment_id=payment.id)


class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
        order = payment.order
        order.status = 'success'
        order.save()

        order_item = OrderItem.objects.filter(order=order)
        for item in order_item:
            product = item.product
            product.stock -= item.quantity
            product.sales_number += item.quantity
            product.save()
        return render(request, 'payment_success.html', {'payment': payment})


class OrderItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        item = get_object_or_404(OrderItem, pk=kwargs['pk'])
        order = item.order

        if order.customer != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)