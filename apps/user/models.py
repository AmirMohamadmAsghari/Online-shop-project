from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .manager import CustomUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedMixin, LogicalMixin


# Create your models her


class CustomUser(AbstractBaseUser, PermissionsMixin, LogicalMixin, TimeStampedMixin):
    username_validator = RegexValidator(
        r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters are allowed."
    )
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True,max_length=150, null=True, validators=[username_validator])
    phone = models.IntegerField(null=True,unique=True)
    otp_code = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    discount_code = models.ForeignKey('CodeDiscount', on_delete=models.CASCADE, related_name='DiscountOrder', null=True, blank=True)
    objects = CustomUserManager()

    class Meta:
        unique_together = [('email', 'username')]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_groups')


class Address(TimeStampedMixin, LogicalMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerAddress')
    name = models.CharField(max_length=255)
    detail_address = models.TextField(max_length=300)
    postal_code = models.IntegerField()
    description = models.TextField(max_length=355)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)

    class Meta:
        ordering = ['user', 'name']

    def __str__(self):
        return f'{self.name} - {self.city} - {self.province}'


class CodeDiscount(LogicalMixin, TimeStampedMixin):
    amount = models.IntegerField(default=0)
    code = models.IntegerField()
