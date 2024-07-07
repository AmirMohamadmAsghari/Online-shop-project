from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from apps.product.models import Product, Category
from django.core.paginator import Paginator
from django.utils.translation import gettext as _, get_language
from django.utils import translation


class Home_View(View):
    template_name = 'home.html'

    def get(self, request):
        discounted_products = Product.objects.filter(discount__isnull=False)

        # Iterate through products to check if associated discount is deleted
        for product in discounted_products:
            if product.discount and product.discount.is_deleted:
                product.discount = None  # Set discount to null if it has been deleted
                product.save()

        paginator = Paginator(discounted_products, 3)  # Show 3 products per page
        page_number = request.GET.get('page')
        paginated_products = paginator.get_page(page_number)

        # Fetch parent categories that have discounts
        discounted_categories = Category.objects.filter(
            discount__isnull=False,
            parent_category__isnull=True,
            discount__is_deleted=False  # Filter out categories where discount is deleted
        ).distinct()

        context = {
            'discounted_products': paginated_products,
            'discounted_categories': discounted_categories,
            'LANGUAGE_CODE': get_language(),
        }
        return render(request, self.template_name, context)


def set_language(request):
    if request.method == 'POST':
        lang_code = request.POST.get('language')
        if lang_code and translation.check_for_language(lang_code):
            next_url = request.POST.get('next', '/')
            response = HttpResponseRedirect(next_url)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response
    return HttpResponseRedirect('/')
