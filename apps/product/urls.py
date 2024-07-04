from django.urls import path
from .views import ProductView, CategoryListAPIView, ProductListAPIView, ImageListAPIView, ProductDetailView, CategoryProductView, ReviewsAPIView



urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/category/<int:category_id>/', CategoryProductView.as_view(), name='category-products'),
    path('productsapi/', ProductListAPIView.as_view(), name='productsapi'),
    path('categoriesapi/', CategoryListAPIView.as_view(), name='categoryapi'),
    path('image/', ImageListAPIView.as_view(), name='imageapi'),
    path('detail/<int:product_id>/', ProductDetailView.as_view(), name='detail'),
    path('api/reviews/<int:product_id>/', ReviewsAPIView.as_view(), name='product-reviews-api'),
]


