# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
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
        # Get the filtering parameters from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Parse the dates and make them timezone aware
        if start_date:
            start_date = parse_datetime(start_date)
            if start_date is not None and timezone.is_naive(start_date):
                start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        if end_date:
            end_date = parse_datetime(end_date)
            if end_date is not None and timezone.is_naive(end_date):
                end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        products = Product.objects.filter(seller=request.user, is_deleted=False)
        deleted_products = Product.objects.deleted().filter(seller=request.user)

        paginator = Paginator(products, 10)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        sales_data = []
        for product in page_obj:
            order_items = OrderItem.objects.filter(product=product)

            # Apply date filtering to the order items
            if start_date:
                order_items = order_items.filter(order__created__gte=start_date)
            if end_date:
                order_items = order_items.filter(order__created__lte=end_date)

            sales_count = sum(item.quantity for item in order_items)
            total_income = sum(item.total_price for item in order_items)
            sales_dates = order_items.values_list('order__created', flat=True)

            sales_data.append({
                'product': product,
                'sales_count': sales_count,
                'total_income': total_income,
                'sales_dates': sales_dates,
            })

        return render(request, 'seller_panel.html', {
            'sales_data': sales_data,
            'page_obj': page_obj,
            'deleted_products': deleted_products,
            'start_date': start_date,
            'end_date': end_date
        })


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