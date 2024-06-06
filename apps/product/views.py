from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Product, Image, Review
from .serializers import ProductSerializer, CategorySerializer, ImageSerializer
from rest_framework import generics, response, permissions, views
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .tasks import my_task


# Create your views here.


class ProductView(View):
    template_name = 'products.html'

    def get(self, request):
        products_list = Product.objects.filter(stock__gt=0)
        paginator = Paginator(products_list, 10)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        parent_categories = Category.objects.filter(parent_category__isnull=True)
        return render(request, self.template_name, {'products': products, 'categories': parent_categories, 'all_products': True})


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
        discounted_price = product.price - product.discount.amount if product.discount else None
        return render(request, self.template_name,
                      {'product': product, 'images': images, 'review': review, 'discounted_price': discounted_price})


def custom_404_view(request, exception):
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


class ReviewsAPIView(View):
    def get(self, request, product_id):
        print("Fetching reviews for product with ID:", product_id)
        # Fetch reviews and related customer user information
        reviews = Review.objects.filter(product_id=product_id).select_related('customer').values('rating',
                                                                                                 'review_Text',
                                                                                                 'customer__username',
                                                                                                 'created')
        print("Fetched reviews:", reviews)
        return JsonResponse(list(reviews), safe=False)
