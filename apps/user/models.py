from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _

# Create your models her


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True)
    phone = models.IntegerField(null=True)
    otp_code = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    session_id = models.IntegerField(blank=True,null=True)
    is_delete = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    # role = models.ForeignKey('UserRole', on_delete=models.CASCADE, null=True, related_name='users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_groups')


# class UserRole(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name


# class CustomPermission(models.Model):
#     action = models.CharField(max_length=255)
#     role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='permissions')
#
#     def __str__(self):
#         return f"{self.action} - {self.role}"


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CustomerAddress')
    name = models.CharField(max_length=255)
    detail_address = models.TextField(max_length=300)
    postal_code = models.IntegerField()
    description = models.TextField(max_length=355)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)