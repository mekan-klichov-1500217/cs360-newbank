from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re

class Account(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def clean(self):
        super().clean()
        # Access the raw password from the instance if it was set
        password = getattr(self, '_password', None)
        if password:
            # 1. Length check
            if len(password) < 8:
                raise ValidationError({'password': 'Password must be at least 8 characters.'})
            
            # 2. Digit check
            if not any(char.isdigit() for char in password):
                raise ValidationError({'password': 'Password must contain at least one digit.'})
                
            # 3. Special character check
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise ValidationError({'password': 'Password must contain at least one special character.'})
            
            # 4. Common sequence check
            if '12345678' in password:
                raise ValidationError({'password': 'Password is too common/weak.'})

    def set_password(self, raw_password):
        self._password = raw_password # Temporarily store raw for validation
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before every save
        super().save(*args, **kwargs)