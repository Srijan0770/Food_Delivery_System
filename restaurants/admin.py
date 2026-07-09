from django.contrib import admin
from .models import Restaurant, Category, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'is_active', 'rating', 'created_at']
    list_filter = ['is_active', 'city', 'category']
    search_fields = ['name', 'city', 'owner__username']
    list_editable = ['is_active']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'rating', 'created_at']
    list_filter = ['rating']
