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
            if len(password) < 8:
                raise ValidationError({'password': 'Password must be at least 8 characters.'})
            # ... rest of your checks ...

    def set_password(self, raw_password):
        self._password = raw_password # Temporarily store raw for validation
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before every save
        super().save(*args, **kwargs)