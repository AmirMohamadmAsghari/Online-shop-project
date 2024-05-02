from django.test import TestCase
from .models import CustomUser, Address

class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'test_user',
            'phone': '1234567890',
            'name': 'Test User',
            'password': 'test_password',
            'is_staff': False,
        }

    def test_create_custom_user(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.phone, self.user_data['phone'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertFalse(user.is_staff)

    # def test_delete_custom_user(self):
    #     user = CustomUser.objects.create(**self.user_data)
    #     user_id = user.id
    #     print(f"User ID before deletion: {user_id}")
    #     user.delete()
    #     print(f"User ID after deletion: {user_id}")
    #     try:
    #         deleted_user = CustomUser.objects.get(id=user_id)
    #     except CustomUser.DoesNotExist:
    #         deleted_user = None
    #     print(f"Deleted user: {deleted_user}")
    #     all_users = CustomUser.objects.all()
    #     print(f"All users after deletion: {all_users}")
    #     self.assertIsNone(deleted_user)
    def test_update_custom_user(self):
        user = CustomUser.objects.create(**self.user_data)
        updated_name = 'Updated Name'
        user.name = updated_name
        user.save()
        updated_user = CustomUser.objects.get(id=user.id)
        self.assertEqual(updated_user.name, updated_name)

class AddressModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'test_user',
            'phone': '1234567890',
            'name': 'Test User',
            'password': 'test_password',
            'is_staff': False,
        }
        self.user = CustomUser.objects.create(**self.user_data)
        self.address_data = {
            'user': self.user,
            'name': 'Home',
            'detail_address': '123 Main St',
            'postal_code': '12345',
            'description': 'My Home Address',
            'city': 'City',
            'province': 'Province',
        }

    def test_create_address(self):
        address = Address.objects.create(**self.address_data)
        self.assertIsInstance(address, Address)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.name, self.address_data['name'])
        self.assertEqual(address.detail_address, self.address_data['detail_address'])
        self.assertEqual(address.postal_code, self.address_data['postal_code'])
        self.assertEqual(address.description, self.address_data['description'])
        self.assertEqual(address.city, self.address_data['city'])
        self.assertEqual(address.province, self.address_data['province'])

    def test_delete_address(self):
        address = Address.objects.create(**self.address_data)
        address_id = address.id
        address.delete()
        with self.assertRaises(Address.DoesNotExist):
            Address.objects.get(id=address_id)

    def test_update_address(self):
        address = Address.objects.create(**self.address_data)
        updated_description = 'Updated Description'
        address.description = updated_description
        address.save()
        updated_address = Address.objects.get(id=address.id)
        self.assertEqual(updated_address.description, updated_description)
