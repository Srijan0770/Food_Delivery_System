from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('delivery_agent', 'Delivery Agent'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_customer(self):
        return self.role == 'customer'

    @property
    def is_restaurant_owner(self):
        return self.role == 'restaurant_owner'

    @property
    def is_delivery_agent(self):
        return self.role == 'delivery_agent'
