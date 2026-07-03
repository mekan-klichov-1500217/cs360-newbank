from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account
from django.core.exceptions import ValidationError

class LoginViewTests(TestCase):
    def setUp(self):
        # Create a user to test login
        self.user = Account.objects.create_user(username='testuser', password='password123')
        self.client = Client()

    def test_login_success(self):
        # Test that valid credentials redirect to my_account
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('accounts:my_account'))

    def test_login_failure(self):
        # Test that invalid credentials show error message
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_login_with_uppercase_username(self):
        # Even if the user created is 'testuser', try logging in with 'TestUser'
        # This will fail if the system enforces strict case-sensitivity or if the view logic doesn't normalize the input.
        response = self.client.post(reverse('accounts:login'), {
            'username': 'TESTUSER', 
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('accounts:my_account'))
    
    def test_password_too_short(self):
        """Test that passwords shorter than 8 characters are rejected."""
        # This will fail if your model currently accepts short passwords
        user = Account.objects.create_user(username='shortuser', password='123')
        # We assume you have a validation method like full_clean()
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_password_no_numbers(self):
        """Test that passwords must contain at least one digit."""
        user = Account.objects.create_user(username='no_number_user', password='password')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_password_common_sequence(self):
        """Test that simple sequences like '12345678' are rejected."""
        user = Account.objects.create_user(username='weakuser', password='12345678')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_password_no_special_chars(self):
        """Test that passwords must contain at least one special character."""
        user = Account.objects.create_user(username='nospecialuser', password='password123')
        with self.assertRaises(ValidationError):
            user.full_clean()