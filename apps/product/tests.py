from django.test import TestCase
from apps.user.models import CustomUser
from .models import Product, Category, Discount, Image, Review


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create(email='seller@example.com', password='password')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            seller=self.seller,
            title='Example Product',
            description='Example description.',
            price=100.0,
            stock=10,
            brand='Example Brand',
            category=self.category
        )

    def test_create_product(self):
        self.assertEqual(Product.objects.count(), 1)

    def test_update_product(self):
        self.product.title = 'Updated Product'
        self.product.save()
        self.assertEqual(Product.objects.get(pk=self.product.pk).title, 'Updated Product')

    def test_delete_product(self):
        self.product.delete()
        self.assertEqual(Product.objects.count(), 0)


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')

    def test_create_category(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_update_category(self):
        self.category.name = 'Updated Category'
        self.category.save()
        self.assertEqual(Category.objects.get(pk=self.category.pk).name, 'Updated Category')

    def test_delete_category(self):
        self.category.delete()
        self.assertEqual(Category.objects.count(), 0)

class DiscountModelTestCase(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(amount=10, type='Percentage', expiration_date='2024-12-31')

    def test_create_discount(self):
        self.assertEqual(Discount.objects.count(), 1)

    def test_update_discount(self):
        self.discount.amount = 20
        self.discount.save()
        self.assertEqual(Discount.objects.get(pk=self.discount.pk).amount, 20)

    def test_delete_discount(self):
        self.discount.delete()
        self.assertEqual(Discount.objects.count(), 0)


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create(email='seller@example.com', password='password')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            seller=self.seller,
            title='Example Product',
            description='Example description.',
            price=100.0,
            stock=10,
            brand='Example Brand',
            category=self.category
        )
        self.image = Image.objects.create(product=self.product, image='example.jpg')

    def test_create_image(self):
        self.assertEqual(Image.objects.count(), 1)

    def test_update_image(self):
        self.image.image = 'updated.jpg'
        self.image.save()
        self.assertEqual(Image.objects.get(pk=self.image.pk).image, 'updated.jpg')

    def test_delete_image(self):
        self.image.delete()
        self.assertEqual(Image.objects.count(), 0)


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create(email='seller@example.com', password='password')
        self.customer = CustomUser.objects.create(email='customer@example.com', password='password')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            seller=self.seller,
            title='Example Product',
            description='Example description.',
            price=100.0,
            stock=10,
            brand='Example Brand',
            category=self.category
        )
        self.review = Review.objects.create(product=self.product, customer=self.customer, rating=4.5, review_Text='Great product!')

    def test_create_review(self):
        self.assertEqual(Review.objects.count(), 1)

    def test_update_review(self):
        self.review.rating = 5.0
        self.review.save()
        self.assertEqual(Review.objects.get(pk=self.review.pk).rating, 5.0)

    def test_delete_review(self):
        self.review.delete()
        self.assertEqual(Review.objects.count(), 0)

