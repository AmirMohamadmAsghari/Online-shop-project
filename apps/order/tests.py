from django.test import TestCase
from .models import Order, OrderItem, CodeDiscount, Payment
from apps.user.models import CustomUser, Address
from apps.product.models import Product, Category

class OrderModelTestCase(TestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create(email='test@example.com', username='testuser')
        self.address = Address.objects.create(user=self.customer, name='Home', detail_address='123 Main St', postal_code='12345', description='Home Address', city='City', province='Province')
        self.order = Order.objects.create(customer=self.customer, total_amount=100.0, address=self.address)

    def test_create_order(self):
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get(customer=self.customer)
        self.assertEqual(order.total_amount, 100.0)
        self.assertEqual(order.status, False)

    def test_update_order(self):
        order = Order.objects.get(customer=self.customer)
        order.status = True
        order.save()
        updated_order = Order.objects.get(customer=self.customer)
        self.assertEqual(updated_order.status, True)

    def test_delete_order(self):
        order = Order.objects.get(customer=self.customer)
        order.delete()
        self.assertEqual(Order.objects.count(), 0)

class OrderItemModelTestCase(TestCase):
    def setUp(self):

        self.customer = CustomUser.objects.create(email='test@example.com', username='testuser')
        self.address = Address.objects.create(user=self.customer, name='Home', detail_address='123 Main St', postal_code='12345', description='Home Address', city='City', province='Province')
        self.order = Order.objects.create(customer=self.customer, total_amount=100.0, address=self.address)
        self.category = Category.objects.create(name='Default Category')
        self.product = Product.objects.create(seller=self.customer, title='Test Product', description='Test Description', price=50.0, stock=10, brand='Brand', category=self.category)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, total_price=100.0)

    def test_create_order_item(self):
        self.assertEqual(OrderItem.objects.count(), 1)
        order_item = OrderItem.objects.get(order=self.order)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.total_price, 100.0)

    def test_update_order_item(self):
        order_item = OrderItem.objects.get(order=self.order)
        order_item.quantity = 3
        order_item.save()
        updated_order_item = OrderItem.objects.get(order=self.order)
        self.assertEqual(updated_order_item.quantity, 3)

    def test_delete_order_item(self):
        order_item = OrderItem.objects.get(order=self.order)
        order_item.delete()
        self.assertEqual(OrderItem.objects.count(), 0)

class CodeDiscountModelTestCase(TestCase):
    def test_create_code_discount(self):
        code_discount = CodeDiscount.objects.create(amount=10, code=12345)
        self.assertEqual(CodeDiscount.objects.count(), 1)
        self.assertEqual(code_discount.amount, 10)
        self.assertEqual(code_discount.code, 12345)

    # Add similar test methods for updating and deleting code discounts

class PaymentModelTestCase(TestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create(email='test@example.com', username='testuser')
        self.address = Address.objects.create(user=self.customer, name='Home', detail_address='123 Main St', postal_code='12345', description='Home Address', city='City', province='Province')
        self.order = Order.objects.create(customer=self.customer, total_amount=100.0, address=self.address)

    def test_create_payment(self):
        payment = Payment.objects.create(order=self.order, payment_type='Credit Card', transaction_id=123456)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(payment.payment_type, 'Credit Card')
        self.assertEqual(payment.transaction_id, 123456)


class PaymentModelTestCase(TestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create(email='test@example.com', username='testuser')
        self.address = Address.objects.create(user=self.customer, name='Home', detail_address='123 Main St', postal_code='12345', description='Home Address', city='City', province='Province')
        self.order = Order.objects.create(customer=self.customer, total_amount=100.0, address=self.address)
        self.payment = Payment.objects.create(order=self.order, payment_type='Credit Card', transaction_id=123456)

    def test_update_payment(self):
        payment = Payment.objects.get(order=self.order)
        payment.payment_type = 'PayPal'
        payment.save()
        updated_payment = Payment.objects.get(order=self.order)
        self.assertEqual(updated_payment.payment_type, 'PayPal')

    def test_delete_payment(self):
        payment = Payment.objects.get(order=self.order)
        payment.delete()
        self.assertEqual(Payment.objects.count(), 0)
