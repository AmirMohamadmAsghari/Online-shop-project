import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from .models import Category, Product, Image, Review
from .serializers import ProductSerializer, CategorySerializer, ImageSerializer
from rest_framework import generics, response, permissions, views
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model



# Create your views here.


class ProductView(View):
    template_name = 'products.html'

    def get(self, request):
        search_query = request.GET.get('search', '')
        products_list = Product.objects.filter(stock__gt=0)

        if search_query:
            products_list = products_list.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(products_list, 9)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        parent_categories = Category.objects.filter(parent_category__isnull=True)
        return render(request, self.template_name, {
            'products': products,
            'categories': parent_categories,
            'all_products': True,
            'search_query': search_query
        })


class CategoryProductView(View):
    template_name = 'products.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        child_categories = Category.objects.filter(parent_category=category)
        products = Product.objects.filter(
            category__in=list(child_categories) + [category],
            stock__gt=0
        )
        parent_categories = Category.objects.filter(parent_category__isnull=True)
        return render(request, self.template_name, {
            'products': products,
            'categories': parent_categories,
            'selected_category': category,
            'child_categories': child_categories
        })


class ProductDetailView(View):
    template_name = 'productdetales.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        images = Image.objects.filter(product_id=product.id)
        review = Review.objects.filter(product_id=product.id)
        discounted_price = product.get_discounted_price()
        return render(request, self.template_name,
                      {'product': product, 'images': images, 'review': review, 'discounted_price': discounted_price})


def custom_404(request, exception):
    return render(request, '404.html', status=404)


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


class ReviewsAPIView(View, LoginRequiredMixin):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id).select_related('customer').values(
            'rating', 'review_Text', 'customer__username', 'created'
        )
        return JsonResponse(list(reviews), safe=False)

    def post(self, request, product_id):
        if request.user.is_authenticated:
            # Handle CSRF token validation
            csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
            if not csrf_token:
                return JsonResponse({'error': 'CSRF token missing'}, status=403)

            # Parse JSON data from request
            data = json.loads(request.body)
            rating = data.get('rating')
            review_text = data.get('reviewText')

            # Create and save new review
            Review.objects.create(
                product_id=product_id,
                customer=request.user,
                rating=rating,
                review_Text=review_text
            )
            print('a')
            return JsonResponse({'success': 'Review submitted successfully'})
        else:
            print('b')
            return JsonResponse({'error': 'You must log in to post a comment'})
