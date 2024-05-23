from django.db import models
from apps.user.models import CustomUser
from apps.product.models import Product
from apps.user.models import Address
from apps.core.models import TimeStampedMixin, LogicalMixin
# Create your models here


class Order(TimeStampedMixin, LogicalMixin):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
        # Add other statuses as needed
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerOrder', null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='AddressesOrder', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

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


class Payment(TimeStampedMixin):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='OrderPayment')
    payment_type = models.CharField(max_length=255)
    transaction_id = models.IntegerField()


