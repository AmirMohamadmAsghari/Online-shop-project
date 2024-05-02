from django.urls import path
from .views import ProductView, CategoryListAPIView, ProductListAPIView, ImageListAPIView, ProductDetailView, ReviewsAPIView

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('productsapi/', ProductListAPIView.as_view(), name='productsapi'),
    path('categoriesapi/', CategoryListAPIView.as_view(), name='categoryapi'),
    path('image/', ImageListAPIView.as_view(), name='imageapi'),
    path('detail/<int:product_id>/', ProductDetailView.as_view(), name='detail'),
    path('api/reviews/<int:product_id>/', ReviewsAPIView.as_view(), name='reviews_api' )
]