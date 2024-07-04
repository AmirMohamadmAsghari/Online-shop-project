from django.shortcuts import render
from django.views import View
from apps.product.models import Product, Category
from django.core.paginator import Paginator


class Home_View(View):
    template_name = 'home.html'

    def get(self, request):
        # Fetch products with discounts
        discounted_products = Product.objects.filter(discount__gt=0)
        paginator = Paginator(discounted_products, 3)  # Show 3 products per page
        page_number = request.GET.get('page')
        paginated_products = paginator.get_page(page_number)

        # Fetch parent categories that have discounts
        discounted_categories = Category.objects.filter(
            discount__isnull=False,
            parent_category__isnull=True
        ).distinct()

        context = {
            'discounted_products': paginated_products,
            'discounted_categories': discounted_categories
        }
        return render(request, self.template_name, context)
