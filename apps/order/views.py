# views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem, Order, Address
from .serializers import OrderItemSerializer, OrderSerializer, AddressSerializer
from .helpers import get_or_create_session_cart
from ..product.models import Product, Image
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


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


def view_orders(request):
    total_items = 0
    total_price = 0
    products = []

    if request.user.is_authenticated:
        cart_orders = Order.objects.filter(customer=request.user, status='open')
        if cart_orders.exists():
            cart_order = cart_orders.first()
            session_cart_order_id = request.session.get('cart_order')
            if session_cart_order_id:
                try:
                    session_cart_order = Order.objects.get(id=session_cart_order_id, status='open')
                    if session_cart_order and session_cart_order != cart_order:
                        for item in OrderItem.objects.filter(order=session_cart_order):
                            existing_item = OrderItem.objects.filter(order=cart_order, product=item.product).first()
                            if existing_item:
                                existing_item.quantity += item.quantity
                                existing_item.total_price += item.total_price
                                existing_item.save()
                            else:
                                OrderItem.objects.create(
                                    order=cart_order,
                                    product=item.product,
                                    quantity=item.quantity,
                                    total_price=item.total_price
                                )
                        session_cart_order.delete()
                        request.session['cart_order'] = cart_order.id
                except Order.DoesNotExist:
                    pass
            products = OrderItem.objects.filter(order=cart_order)
        else:
            cart_order = get_or_create_session_cart(request)
            products = OrderItem.objects.filter(order=cart_order)
    else:
        cart_order = get_or_create_session_cart(request)
        products = OrderItem.objects.filter(order=cart_order)

    for product in products:
        total_items += product.quantity
        total_price += product.quantity * product.product.price

    images = Image.objects.filter(product__in=[item.product for item in products])

    return render(request, 'orders.html', {
        'cart_orders': [cart_order] if cart_order else [],
        'products': products,
        'total_items': total_items,
        'total_price': total_price,
        'images': images
    })

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
        if request.user.is_authenticated:
            cart_id = request.session.get('cart_id')
            if cart_id:
                try:
                    cart_order = Order.objects.get(id=cart_id, status='open')
                    user_order, created = Order.objects.get_or_create(customer=request.user, status='open')

                    for item in OrderItem.objects.filter(order=cart_order):
                        item.order = user_order
                        item.save()

                    cart_order.delete()
                    del request.session['cart_id']
                except Order.DoesNotExist:
                    pass

            return HttpResponse("Checkout page content")
        else:
            login_url = reverse('login')
            return redirect(login_url)
