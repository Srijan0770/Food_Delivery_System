from django.contrib import admin
from .models import MenuItem, MenuCategory


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'is_available', 'is_vegetarian']
    list_filter = ['is_available', 'is_vegetarian', 'is_vegan', 'is_spicy']
    search_fields = ['name', 'restaurant__name']
    list_editable = ['is_available', 'price']
