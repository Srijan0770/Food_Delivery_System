from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item_name', 'item_price', 'quantity', 'get_subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant', 'status', 'total_amount', 'payment_method', 'is_paid', 'created_at']
    list_filter = ['status', 'payment_method', 'is_paid']
    search_fields = ['user__username', 'restaurant__name']
    list_editable = ['status', 'is_paid']
    inlines = [OrderItemInline]
    readonly_fields = ['subtotal', 'delivery_charge', 'total_amount', 'created_at']
