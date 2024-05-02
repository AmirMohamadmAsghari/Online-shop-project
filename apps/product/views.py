from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Product, Image, Review
from .serializers import ProductSerializer, CategorySerializer, ImageSerializer
from rest_framework import generics, response, permissions
from django.contrib.auth import get_user_model


# Create your views here.


class ProductView(View):
    template_name = 'products.html'

    def get(self, request):
        products = Product.objects.all()
        images = Image.objects.all()
        categories = Category.objects.all()
        return render(request, self.template_name, {'products': products, 'images': images, 'categories': categories})


class ProductDetailView(View):
    template_name = 'productdetales.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        images = Image.objects.filter(product_id=product.id)
        review = Review.objects.filter(product_id=product.id)
        return render(request, self.template_name, {'product': product, 'images':images, 'review': review})

# =====================API_View=====================


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ReviewsAPIView(View):
    def get(self, request, product_id):
        print("Fetching reviews for product with ID:", product_id)
        # Fetch reviews and related customer user information
        reviews = Review.objects.filter(product_id=product_id).select_related('customer').values('rating', 'review_Text', 'customer__username', 'created')
        print("Fetched reviews:", reviews)
        return JsonResponse(list(reviews), safe=False)