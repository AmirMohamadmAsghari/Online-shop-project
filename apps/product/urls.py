from django.urls import path
from .views import ProductView, CategoryListAPIView, ProductListAPIView, ImageListAPIView, ProductDetailView, CategoryProductView, ReviewsAPIView
from django.conf.urls import handler404
from .views import custom_404_view

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/category/<int:category_id>/', CategoryProductView.as_view(), name='category-products'),
    path('productsapi/', ProductListAPIView.as_view(), name='productsapi'),
    path('categoriesapi/', CategoryListAPIView.as_view(), name='categoryapi'),
    path('image/', ImageListAPIView.as_view(), name='imageapi'),
    path('detail/<int:product_id>/', ProductDetailView.as_view(), name='detail'),
    path('api/reviews/<int:product_id>/', ReviewsAPIView.as_view(), name='reviews_api')
]

handler404 = custom_404_view
