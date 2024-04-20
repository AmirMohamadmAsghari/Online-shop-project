from django.contrib import admin
from .models import Order, OrderItem, CodeDiscount, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'order_date', 'status')
    search_fields = ('customer__email', 'order_date')
    list_filter = ('status', 'order_date')
    inlines = [OrderItemInline]


class CodeDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'code', 'is_deleted')
    search_fields = ('code',)
    list_filter = ('is_deleted',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_date', 'payment_type', 'transaction_id')
    search_fields = ('order__id', 'payment_date')
    list_filter = ('payment_date', 'payment_type')




admin.site.register(Order, OrderAdmin)
admin.site.register(CodeDiscount, CodeDiscountAdmin)
admin.site.register(Payment, PaymentAdmin)

