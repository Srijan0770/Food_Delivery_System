from django.db import models
from accounts.models import User
from menu.models import MenuItem
from restaurants.models import Restaurant


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    delivery_agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    is_paid = models.BooleanField(default=False)

    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_phone = models.CharField(max_length=15)
    special_instructions = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    def get_status_color(self):
        colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'preparing': 'primary',
            'out_for_delivery': 'secondary',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200)  # snapshot at time of order
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"

    def get_subtotal(self):
        return self.item_price * self.quantity
