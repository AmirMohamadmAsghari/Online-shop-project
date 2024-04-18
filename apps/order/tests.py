from datetime import datetime
from django.test import TestCase
from apps.user.models import CustomUser
from apps.product.models import Product, Category
from .models import Order, OrderItem, Address, Payment, CodeDiscount


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a CustomUser instance for testing
        self.user = CustomUser.objects.create(email='test@example.com', username='testuser', password='password')

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
            category=self.category  # Include the category field
        )

        # Create a CodeDiscount instance for testing
        self.discount = CodeDiscount.objects.create(amount=10, code=1234)

        # Create an Address instance for testing
        self.address = Address.objects.create(
            user=self.user,
            name='Test Address',
            detail_address='123 Test Street',
            postal_code=12345,
            description='Test address description',
            city='Test City',
            province='Test Province'
        )

        # Create an Order instance for testing
        self.order = Order.objects.create(
            customer=self.user,
            total_amount=100.00,
            address=self.address,
            order_date=datetime.now(),
            discount_code=self.discount,
            status=False,
            session_id=12345
        )

        # Create an OrderItem instance for testing
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            total_price=200.00
        )

        # Create a Payment instance for testing
        self.payment = Payment.objects.create(
            order=self.order,
            payment_date=datetime.now(),
            payment_type='Credit Card',
            transaction_id='123456789'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.user)
        self.assertEqual(self.order.total_amount, 100.00)
        self.assertEqual(self.order.address, self.address)
        self.assertFalse(self.order.status)  # Asserting that status is initially False

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.total_price, 200.00)

    def test_address_creation(self):
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.name, 'Test Address')
        self.assertEqual(self.address.detail_address, '123 Test Street')
        self.assertEqual(self.address.postal_code, 12345)
        self.assertEqual(self.address.description, 'Test address description')
        self.assertEqual(self.address.city, 'Test City')
        self.assertEqual(self.address.province, 'Test Province')

    def test_payment_creation(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.payment_type, 'Credit Card')
        self.assertEqual(self.payment.transaction_id, '123456789')
