from django.contrib import admin
from .models import Product, Category, Discount, Image, Review


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'price', 'stock', 'category', 'is_delete')
    search_fields = ('title', 'seller__email', 'category__name')
    list_filter = ('seller', 'category', 'is_delete')
    inlines = [ImageInline, ReviewInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category', 'discount', 'is_delete')
    search_fields = ('name', 'parent_category__name')
    list_filter = ('parent_category', 'is_delete')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'type', 'is_deleted')
    search_fields = ('type',)
    list_filter = ('type', 'is_deleted')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'rating', 'review_Date', 'is_delete')
    search_fields = ('product__title', 'customer__email')
    list_filter = ('rating', 'review_Date', 'is_delete')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Review, ReviewAdmin)
