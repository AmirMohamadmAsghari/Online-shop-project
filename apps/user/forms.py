from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from .models import CustomUser


class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'name')


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')