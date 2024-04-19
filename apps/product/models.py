from django.db import models
from apps.user.models import CustomUser

# Create your models here.


class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='SellerProducts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sales_number = models.IntegerField(default=0)
    brand = models.CharField(max_length=255)
    discount = models.OneToOneField('Discount',on_delete=models.CASCADE,null=True, blank=True, related_name='DiscountP')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='CategoryProducts')
    is_delete = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    discount = models.OneToOneField('Discount', on_delete=models.CASCADE, null=True, blank=True)
    is_delete = models.BooleanField(default=False)


class Discount(models.Model):
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ProductImages')
    image = models.ImageField(upload_to='storage/ProductImages')


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ProductReviews')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerReviews')
    rating = models.DecimalField(max_digits=10, decimal_places=2)
    review_Text = models.TextField()
    review_Date = models.DateField(auto_now=True)
    is_delete = models.BooleanField(default=False)