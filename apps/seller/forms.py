from django import forms
from apps.product.models import Product, Image


class SalesFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock', 'brand', 'discount', 'category', 'seller']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['seller'].queryset = self.fields['seller'].queryset.filter(id=user.id)
            self.fields['seller'].initial = user.id
            self.fields['seller'].widget = forms.HiddenInput()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']