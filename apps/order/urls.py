from django.urls import path
from .views import OrderItemCreate, OrderAPIView, AddressAPIView, AddToCartView, CheckOutView, OrderView, PaymentInitiateView, PaymentSuccessView, OrderItemDeleteView

urlpatterns = [
    path('orderitem', OrderItemCreate.as_view(), name='orderitem'),
    path('order',OrderAPIView.as_view(), name='order'),
    path('address', AddressAPIView.as_view(), name='address'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/order-item/<int:pk>/', OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('view-order/', OrderView.as_view(), name='view-order'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('payment/<int:order_id>/initiate', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('payment/<int:payment_id>/success/', PaymentSuccessView.as_view(), name='payment-success'),
]