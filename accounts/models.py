from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re

class Account(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def set_password(self, raw_password):
        self._password = raw_password  # Store raw for validation
        super().set_password(raw_password)

    def clean(self):
        super().clean()
        # Fallback to None if _password isn't set
        password = getattr(self, '_password', None)
        
        # Only validate if a raw password was provided
        if password:
            if len(password) < 8:
                raise ValidationError({'password': 'Password must be at least 8 characters.'})
            if not any(char.isdigit() for char in password):
                raise ValidationError({'password': 'Password must contain at least one digit.'})
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise ValidationError({'password': 'Password must contain at least one special character.'})
            if '12345678' in password:
                raise ValidationError({'password': 'Password is too common/weak.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before every save
        super().save(*args, **kwargs)