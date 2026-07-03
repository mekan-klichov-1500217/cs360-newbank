from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account

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