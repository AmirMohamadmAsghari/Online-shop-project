# helpers.py
from .models import Order
from django.contrib.auth.signals import  user_logged_in
from django.dispatch import receiver

def get_or_create_session_cart(request):
    cart_order_id = request.session.get('cart_order')
    if cart_order_id:
        try:
            cart_order = Order.objects.get(id=cart_order_id, status='open')
            cart_order.customer_id = request.user.id
        except Order.DoesNotExist:
            cart_order = Order.objects.create(status='open')
            request.session['cart_order'] = cart_order.id
    else:
        cart_order = Order.objects.create(status='open')
        request.session['cart_order'] = cart_order.id
    return cart_order


@receiver(user_logged_in)
def merge_order_with_user(sender, user, request, **kwargs):
    if 'cart_order' in request.session:
        cart_order_id = request.session['cart_order']
        try:
            cart_order = Order.objects.get(id=cart_order_id,status='open')
            cart_order.customer_id = user
            cart_order.save()
        except Order.DoesNotExist:
            pass