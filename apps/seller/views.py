# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.product.models import Product, Image
from apps.order.models import OrderItem
from .forms import ProductForm, ImageForm, SalesFilterForm
from django.core.paginator import Paginator
from django.http import JsonResponse


class SellerPanelView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Sellers').exists()

    def get(self, request):
        products = Product.objects.filter(seller=request.user, is_deleted=False)
        deleted_products = Product.objects.filter(seller=request.user, is_deleted=True)
        print(deleted_products)
        paginator = Paginator(products, 10)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        sales_data = []
        for product in page_obj:
            order_items = OrderItem.objects.filter(product=product)
            sales_count = sum(item.quantity for item in order_items)
            total_income = sum(item.total_price for item in order_items)
            sales_dates = order_items.values_list('order__created', flat=True)

            sales_data.append({
                'product': product,
                'sales_count': sales_count,
                'total_income': total_income,
                'sales_dates': sales_dates,
            })

        return render(request, 'seller_panel.html', {'sales_data': sales_data, 'page_obj': page_obj, 'deleted_products': deleted_products})


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Sellers').exists()

    def get(self, request):
        product_form = ProductForm(user=request.user)
        image_form = ImageForm()
        return render(request, 'product_form.html', {'product_form': product_form, 'image_form': image_form})

    def post(self, request):
        product_form = ProductForm(request.POST, request.FILES, user=request.user)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user
            product.save()

            for file in request.FILES.getlist('image'):
                image = Image(product=product, image=file)
                image.save()

            return redirect('seller-panel')
        return render(request, 'product_form.html', {'product_form': product_form})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Sellers').exists()

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        product_form = ProductForm(instance=product, user=request.user)
        image_form = ImageForm()
        return render(request, 'product_form.html', {'product_form': product_form, 'image_form': image_form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        product_form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if product_form.is_valid():
            product_form.save()

            for file in request.FILES.getlist('image'):
                image = Image(product=product, image=file)
                image.save()

            return redirect('seller-panel')
        return render(request, 'product_form.html', {'product_form': product_form})


class DeleteProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, seller=request.user)
        product.is_deleted = True
        product.is_active = False
        product.save()
        return redirect('seller-panel')

class PermanentDeleteProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, seller=request.user, is_deleted=True)
        product.delete()
        return redirect('seller-panel')