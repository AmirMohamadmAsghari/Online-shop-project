from django.contrib import admin
from .models import Product, Category, Discount, Image, Review


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'price', 'stock', 'category')
    search_fields = ('title', 'seller__email', 'category__name')
    #list_filter = ('seller', 'category')
    inlines = [ImageInline, ReviewInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category', 'discount')
    search_fields = ('name', 'parent_category__name')
    #list_filter = ('parent_category')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'type')
    search_fields = ('type',)
    #list_filter = ('type')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'rating', 'created')
    search_fields = ('product__title', 'customer__email')
    #list_filter = ('rating', 'created')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Review, ReviewAdmin)
