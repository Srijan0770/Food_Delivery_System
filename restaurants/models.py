from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='🍽️')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    opening_time = models.TimeField(default='09:00')
    closing_time = models.TimeField(default='22:00')
    delivery_time = models.PositiveIntegerField(default=30, help_text='Estimated delivery time in minutes')
    minimum_order = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating}★)"
