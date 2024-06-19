# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.db import transaction
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem, Order, Address, Payment, CodeDiscount
from .serializers import OrderItemSerializer, OrderSerializer, AddressSerializer
from .helpers import get_or_create_session_cart
from ..product.models import Product, Image
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import logging
import json
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'product_id': product.id,
                'quantity': quantity,
                'price': float(product.price),
                'title': product.title
            }

        request.session['cart'] = cart
        request.session.modified = True

        return Response(cart, status=status.HTTP_201_CREATED)


class OrderView(View):
    def get(self, request):
        cart_details = self.get_cart_details(request)
        product_images = self.get_images_for_products(cart_details['products'])

        return render(request, 'orders.html', {
            'products': cart_details['products'],
            'total_items': cart_details['total_items'],
            'total_price': cart_details['total_price'],
            'images': product_images
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            product_id = int(data.get('product_id'))

            if action == 'increase':
                self.increase_quantity(request, product_id)
            elif action == 'decrease':
                self.decrease_quantity(request, product_id)

            cart_details = self.get_cart_details(request)
            product_images = self.get_images_for_products(cart_details['products'])

            html = render_to_string('orders.html', {
                'products': cart_details['products'],
                'total_items': cart_details['total_items'],
                'total_price': cart_details['total_price'],
                'images': product_images
            }, request)

            return JsonResponse({'html': html})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def increase_quantity(self, request, product_id):
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            product = get_object_or_404(Product, pk=product_id)
            if cart[str(product_id)]['quantity'] < product.stock:
                cart[str(product_id)]['quantity'] += 1
                request.session['cart'] = cart
            else:
                # Handle insufficient stock scenario (optional)
                # You can raise an error or display a message to the user
                messages.error(request, 'Insufficient stock available.')
        else:
            # Handle case where product is not in cart (optional)
            messages.error(request, 'Product not found in cart.')

    def decrease_quantity(self, request, product_id):
        cart = request.session.get('cart', {})
        if str(product_id) in cart and cart[str(product_id)]['quantity'] > 0:
            cart[str(product_id)]['quantity'] -= 1
        if cart[str(product_id)]['quantity'] == 0:
            del cart[str(product_id)]
        request.session['cart'] = cart

    def get_cart_details(self, request):
        cart = request.session.get('cart', {})
        total_items = 0
        total_price = 0
        products = []

        for item in cart.values():
            product = Product.objects.get(id=item['product_id'])
            quantity = item['quantity']
            price = product.price
            discounted_price = product.get_discounted_price()  # Replace with your method to calculate discounted price

            # Calculate total price for the item considering quantity and discounted price
            total_price_item = discounted_price * quantity

            total_items += quantity
            total_price += total_price_item

            products.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'discounted_price': discounted_price,
                'total_price': total_price_item  # Use total_price_item here
            })

        return {
            'total_items': total_items,
            'total_price': total_price,
            'products': products
        }

    def get_images_for_products(self, products):
        product_ids = [item['product'].id for item in products]
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
        selected_address_id = request.session.get('selected_address_id')
        if not selected_address_id:
            messages.error(request, 'Please select an address before proceeding to checkout.')
            return redirect('address-list')

        try:
            address = Address.objects.get(id=selected_address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, 'Selected address not found.')
            return redirect('address-list')

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Your cart is empty.')
            return redirect('view-order')

        # Calculate total amount with discounts applied
        total_amount = 0

        for item in cart.values():
            product = Product.objects.get(id=item['product_id'])
            discounted_price = product.get_discounted_price()  # Calculate discounted price
            total_amount += item['quantity'] * discounted_price

        # Check if there's an existing open order
        try:
            order = Order.objects.get(customer=request.user, status='open')
            order.total_amount = total_amount
            order.address = address
            order.save()
        except Order.DoesNotExist:
            order = Order.objects.create(
                customer=request.user,
                total_amount=total_amount,
                address=address,
                status='open'
            )

        # Clear existing order items if updating an existing order
        order.OrderItem.all().delete()

        for item in cart.values():
            product = Product.objects.get(id=item['product_id'])
            discounted_price = product.get_discounted_price()  # Calculate discounted price
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                total_price=item['quantity'] * discounted_price  # Use discounted price here
            )

        print(request.session['cart'])
        print(request.session['selected_address_id'])

        return redirect('payment-initiate', order_id=order.id)


class PaymentInitiateView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            return render(request, 'payment_initiate.html', {'order': order})
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('view-order')

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            payment_type = request.POST.get('payment_type', 'Not Specified')
            transaction_id = request.POST.get('transaction_id', 'Not Specified')
            discount_code = request.POST.get('discount_code')

            with transaction.atomic():
                # Apply discount code if provided
                if discount_code:
                    try:
                        code_discount = CodeDiscount.objects.get(code=discount_code)
                        if code_discount.is_active:
                            if order.total_amount >= code_discount.minimum_purchase_amount:
                                if code_discount.type == 'percentage':
                                    discount_amount = (code_discount.amount / 100) * order.total_amount
                                elif code_discount.type == 'fixed':
                                    discount_amount = code_discount.amount
                                # Apply the discount
                                order.total_amount = max(order.total_amount - discount_amount, 0)
                                order.discount_code = code_discount.code
                                # Deactivate the discount code
                                code_discount.is_active = False
                                # Save the order and discount code
                                order.save()
                                code_discount.save()
                            else:
                                messages.error(request,
                                               f"Minimum purchase amount for this discount code is ${code_discount.minimum_purchase_amount}.")
                                return redirect('payment-initiate', order_id=order.id)
                        else:
                            messages.error(request, 'This discount code is no longer active.')
                            return redirect('payment-initiate', order_id=order.id)
                    except CodeDiscount.DoesNotExist:
                        messages.error(request, 'Invalid discount code.')
                        return redirect('payment-initiate', order_id=order.id)

                # Create a Payment object to store payment details
                payment = Payment.objects.create(
                    payment_type=payment_type,
                    transaction_id=transaction_id,
                    order=order,
                    amount=order.total_amount,
                    status='pending'
                )

                return redirect('payment-success', payment_id=payment.id)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('view-order')


class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
        order = payment.order
        order.status = 'success'
        order.save()

        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            product.stock -= item.quantity
            product.sales_number += item.quantity
            product.save()

        del request.session['cart']
        del request.session['selected_address_id']

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
