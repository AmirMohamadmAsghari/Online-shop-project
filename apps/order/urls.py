from django.urls import path
from .views import OrderItemCreate, OrderAPIView, AddressAPIView, AddToCartView, view_orders, CheckOutView

urlpatterns = [
    path('orderitem', OrderItemCreate.as_view(), name='orderitem'),
    path('order',OrderAPIView.as_view(), name='order'),
    path('address', AddressAPIView.as_view(), name='address'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('view-order', view_orders, name='view-order'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
]