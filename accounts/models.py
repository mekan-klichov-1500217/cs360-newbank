from django.db import models
from django.core.exceptions import ValidationError

class Account(models.Model):
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def clean(self):
        # 1. Empty input validation
        if not self.account_number:
            raise ValidationError({'account_number': 'Account number cannot be empty.'})
        
        # 2. Negative balance validation
        if self.balance < 0:
            raise ValidationError({'balance': 'Balance cannot be negative.'})
            
        # 3. Format validation (e.g., must be digits only)
        if not self.account_number.isdigit():
            raise ValidationError({'account_number': 'Account number must be numeric.'})

    def __str__(self):
        return f"{self.account_number}"