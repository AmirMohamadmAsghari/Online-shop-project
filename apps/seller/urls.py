from django.urls import path
from .views import SellerPanelView, ProductCreateView, ProductUpdateView, DeleteProductView, PermanentDeleteProductView, CreateDiscountCodeView

urlpatterns = [
    path('seller-panel/', SellerPanelView.as_view(), name='seller-panel'),
    path('product/add/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('product/<int:product_id>/delete/', DeleteProductView.as_view(), name='delete-product'),
    path('product/<int:product_id>/permanent-delete/', PermanentDeleteProductView.as_view(), name='permanent-delete-product'),
    path('create-discount/', CreateDiscountCodeView.as_view(), name='create_discount'),
]