from django.db import models
from apps.user.models import CustomUser
from apps.product.models import Product
from apps.user.models import Address, CodeDiscount
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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='AddressesOrder', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    discount_code = models.CharField(max_length=255, null=True, blank=True)

    def update_total_amount(self):
        base_total = sum(item.quantity * item.price for item in self.item.all())

        discount = None
        if self.discount_code:
            try:
                discount = CodeDiscount.objects.get(code=self.discount_code)
                if base_total >= discount.minimum_purchase_amount:
                    if discount.type == 'percentage':
                        discount_amount = (discount.amount / 100) * base_total
                    elif discount.type == 'fixed':
                        discount_amount = discount.amount
                    base_total -= discount_amount
            except CodeDiscount.DoesNotExist:
                pass  # Invalid discount code, ignore it

        self.total_amount = max(base_total, 0)  # Ensure the total amount is not negative
        self.save()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(fields=['customer'], condition=models.Q(status='open'), name='unique_open_order_per_customer')
        ]

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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')


