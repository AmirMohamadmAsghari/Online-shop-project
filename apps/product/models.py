from django.db import models
from decimal import Decimal
from apps.user.models import CustomUser
from apps.core.models import TimeStampedMixin, LogicalMixin
from django.conf import settings
# Create your models here.


class Product(TimeStampedMixin, LogicalMixin):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='SellerProducts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sales_number = models.IntegerField(default=0)
    brand = models.CharField(max_length=255)
    discount = models.ForeignKey('Discount',on_delete=models.CASCADE,null=True, blank=True, related_name='DiscountP')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='CategoryProducts')

    def get_discounted_price(self):
        original_price = self.price

        # Apply product discount
        if self.discount and not self.discount.is_deleted:
            if self.discount.type == 'percentage':
                discount_value = (Decimal(self.discount.amount) / Decimal(100)) * original_price
                original_price -= discount_value
            elif self.discount.type == 'fixed':
                original_price -= Decimal(self.discount.amount)

        # Apply category discounts
        category = self.category
        while category:
            if category.discount and not category.discount.is_deleted:
                if category.discount.type == 'percentage':
                    discount_value = (Decimal(category.discount.amount) / Decimal(100)) * original_price
                    original_price -= discount_value
                elif category.discount.type == 'fixed':
                    original_price -= Decimal(category.discount.amount)
            category = category.parent_category

        return max(original_price, Decimal(0))


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['created']

    def __str__(self):
        return self.title


class Category(TimeStampedMixin, LogicalMixin):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Discount(TimeStampedMixin, LogicalMixin):
    STATUS_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    ]
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=255,choices=STATUS_CHOICES)
    expiration_date = models.DateField()

    class Meta:
        verbose_name = 'Discount'
        ordering = ['created']


class Image(TimeStampedMixin):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ProductImages')
    image = models.ImageField(upload_to='storage/ProductImages')


class Review(TimeStampedMixin, LogicalMixin):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ProductReviews')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerReviews')
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    review_Text = models.TextField()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created']

    def __str__(self):
        return f"Review for {self.product} by {self.customer}"


