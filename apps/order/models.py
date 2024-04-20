from django.db import models
from apps.user.models import CustomUser
from apps.product.models import Product
from apps.user.models import Address
# Create your models here


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerOrder')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='AddressesOrder')
    order_date = models.DateTimeField(auto_now_add=True)
    discount_code = models.ForeignKey('CodeDiscount', on_delete=models.CASCADE, related_name='DiscountOrder', null=True, blank=True)
    status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='OrderItem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ProductOrder')
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)


class CodeDiscount(models.Model):
    amount = models.IntegerField(default=0)
    code = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='OrderPayment')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=255)
    transaction_id = models.IntegerField()


