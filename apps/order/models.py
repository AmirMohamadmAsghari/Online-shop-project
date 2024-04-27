from django.db import models
from apps.user.models import CustomUser
from apps.product.models import Product
from apps.user.models import Address
from apps.core.models import TimeStampedMixin, LogicalMixin
# Create your models here


class Order(TimeStampedMixin, LogicalMixin):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerOrder')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='AddressesOrder')
    discount_code = models.ForeignKey('CodeDiscount', on_delete=models.CASCADE, related_name='DiscountOrder', null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created']

    def __str__(self):
        return f"Order {self.id} by {self.customer}"


class OrderItem(TimeStampedMixin, LogicalMixin):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='OrderItem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ProductOrder')
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "OrderItem"
        ordering = ["-created"]


class CodeDiscount(LogicalMixin, TimeStampedMixin):
    amount = models.IntegerField(default=0)
    code = models.IntegerField()


class Payment(TimeStampedMixin):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='OrderPayment')
    payment_type = models.CharField(max_length=255)
    transaction_id = models.IntegerField()


