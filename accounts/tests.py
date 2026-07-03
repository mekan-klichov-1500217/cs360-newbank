from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import Account

class AccountRegistrationTests(TestCase):
    def test_account_validation_scenarios(self):
        # Define test cases: (data, expected_error_key)
        scenarios = [
            ({'account_number': '', 'balance': 100}, 'account_number'), # Empty input
            ({'account_number': '123', 'balance': -50}, 'balance'),    # Negative balance
            ({'account_number': 'ABC', 'balance': 100}, 'account_number'), # Invalid format
            ({'account_number': '12345', 'balance': 0}, None),         # Valid case
        ]

        for data, expected_error in scenarios:
            with self.subTest(data=data):
                account = Account(**data)
                if expected_error:
                    with self.assertRaises(ValidationError):
                        account.full_clean()
                else:
                    # Should pass for the valid scenario
                    account.full_clean()