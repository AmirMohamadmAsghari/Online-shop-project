from django.test import TestCase
from .models import Product, Category, Discount, Image, Review
from apps.user.models import CustomUser
from datetime import date


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a CustomUser instance for testing
        self.user = CustomUser.objects.create(email='test@example.com', username='testuser', password='password')

        # Create a Discount instance for testing
        self.discount = Discount.objects.create(amount=10, type='Percentage')

        # Create a Category instance for testing
        self.category = Category.objects.create(name='Electronics')

        # Create a Product instance for testing
        self.product = Product.objects.create(
            seller=self.user,
            title='Test Product',
            description='This is a test product',
            price=100.00,
            stock=50,
            brand='Test Brand',
            discount=self.discount,
            category=self.category
        )

        # Create an Image instance for testing
        self.image = Image.objects.create(product=self.product, image='path/to/image.jpg')

        # Create a Review instance for testing
        self.review = Review.objects.create(
            product=self.product,
            customer=self.user,
            rating=4.5,
            review_Text='This is a test review',
            review_Date=date.today()
        )

    def test_product_creation(self):
        def test_product_creation(self):
            # Assert product attributes
            self.assertEqual(self.product.title, 'Test Product')
            self.assertEqual(self.product.seller, self.user)
            self.assertEqual(self.product.description, 'This is a test product')
            self.assertEqual(self.product.price, 100.00)
            self.assertEqual(self.product.stock, 50)
            self.assertEqual(self.product.brand, 'Test Brand')
            self.assertEqual(self.product.discount, self.discount)
            self.assertEqual(self.product.category, self.category)
            self.assertEqual(self.product.ProductImages.first(), self.image)
            self.assertEqual(self.product.ProductReviews.first(), self.review)

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')


    def test_discount_creation(self):
        self.assertEqual(self.discount.amount, 10)
        self.assertEqual(self.discount.type, 'Percentage')

    def test_image_creation(self):
        self.assertEqual(self.image.product, self.product)

    def test_review_creation(self):
        self.assertEqual(self.review.customer, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating,4.5)
        self.assertEqual(self.review.review_Text,'This is a test review')

