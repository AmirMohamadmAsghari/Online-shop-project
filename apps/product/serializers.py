from rest_framework import serializers
from .models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['is_active', 'is_deleted', 'modified']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['is_active', 'is_deleted', 'modified']


class ImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Image
        fields = '__all__'
