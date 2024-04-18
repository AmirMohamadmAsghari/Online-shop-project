from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser, UserRole, CustomPermission

class ModelTestCase(TestCase):
    def setUp(self):
        # Create a UserRole instance for testing
        self.user_role = UserRole.objects.create(name='Admin')

        # Create a CustomUser instance for testing
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password',
            phone=1234567890,
            otp_code=1234,
            name='Test User',
            session_id=12345,
            is_delete=False,
            is_staff=True,
            is_active=True,
            role=self.user_role
        )

        # Create a CustomPermission instance for testing
        self.permission = CustomPermission.objects.create(action='Can add user', role=self.user_role)

    def test_user_role_creation(self):
        self.assertEqual(self.user_role.name, 'Admin')

    def test_custom_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.phone, 1234567890)
        self.assertEqual(self.user.otp_code, 1234)
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.session_id, 12345)
        self.assertFalse(self.user.is_delete)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.role, self.user_role)

    def test_custom_permission_creation(self):
        self.assertEqual(self.permission.action, 'Can add user')
        self.assertEqual(self.permission.role, self.user_role)
