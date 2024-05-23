from django.contrib import admin
from .models import Order, OrderItem, Payment
from apps.user.models import CodeDiscount


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'created')
    search_fields = ('customer__email', 'created')
    # list_filter = 'created'
    inlines = [OrderItemInline]


class CodeDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'code')
    search_fields = ('code',)
    #list_filter = ('is_deleted')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'created', 'payment_type', 'transaction_id')
    search_fields = ('order__id', 'created')
    #list_filter = ('created', 'payment_type')




admin.site.register(Order, OrderAdmin)
admin.site.register(CodeDiscount, CodeDiscountAdmin)
admin.site.register(Payment, PaymentAdmin)

