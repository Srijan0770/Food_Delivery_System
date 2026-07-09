"""
Run this script to create a superuser and seed sample data:
    python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fooddelivery.settings')
django.setup()

from accounts.models import User
from restaurants.models import Category, Restaurant
from menu.models import MenuCategory, MenuItem

# Create superuser
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@foodexpress.com',
        password='admin123',
        role='restaurant_owner',
    )
    print("✅ Superuser created: admin / admin123")
else:
    admin = User.objects.get(username='admin')
    print("ℹ️  Superuser already exists.")

# Create categories
categories_data = [
    ('Pizza', '🍕'), ('Burgers', '🍔'), ('Chinese', '🍜'),
    ('Sushi', '🍣'), ('Indian', '🍛'), ('Desserts', '🍰'),
    ('Salads', '🥗'), ('Biryani', '🍚'),
]
for name, icon in categories_data:
    Category.objects.get_or_create(name=name, defaults={'icon': icon})
print("✅ Categories created.")

# Create menu categories
menu_cats = ['Starters', 'Main Course', 'Beverages', 'Desserts', 'Sides']
for name in menu_cats:
    MenuCategory.objects.get_or_create(name=name)
print("✅ Menu categories created.")

# Create sample restaurant
if not Restaurant.objects.filter(name="Spice Garden").exists():
    cat = Category.objects.get(name='Indian')
    restaurant = Restaurant.objects.create(
        owner=admin,
        name="Spice Garden",
        description="Authentic Indian cuisine with rich flavours and aromatic spices.",
        address="12 MG Road",
        city="Kolkata",
        phone="9876543210",
        email="spicegarden@example.com",
        category=cat,
        delivery_time=35,
        minimum_order=150,
        delivery_charge=30,
    )

    starter = MenuCategory.objects.get(name='Starters')
    main = MenuCategory.objects.get(name='Main Course')
    bev = MenuCategory.objects.get(name='Beverages')

    items = [
        (starter, "Paneer Tikka", "Grilled cottage cheese with spices", 180, True, False, True),
        (starter, "Chicken Tikka", "Tender chicken marinated in yogurt", 220, False, False, True),
        (main, "Butter Chicken", "Creamy tomato-based chicken curry", 280, False, False, False),
        (main, "Dal Makhani", "Slow-cooked black lentils in butter", 200, True, False, False),
        (main, "Veg Biryani", "Fragrant basmati rice with vegetables", 220, True, False, False),
        (bev, "Mango Lassi", "Chilled yogurt mango drink", 80, True, False, False),
        (bev, "Masala Chai", "Spiced Indian tea", 40, True, False, False),
    ]
    for cat_obj, name, desc, price, veg, vegan, spicy in items:
        MenuItem.objects.create(
            restaurant=restaurant,
            category=cat_obj,
            name=name,
            description=desc,
            price=price,
            is_vegetarian=veg,
            is_vegan=vegan,
            is_spicy=spicy,
        )
    print("✅ Sample restaurant 'Spice Garden' with menu created.")
else:
    print("ℹ️  Sample restaurant already exists.")

print("\n🚀 Setup complete! Run: python manage.py runserver")
print("   Admin panel: http://127.0.0.1:8000/admin/  (admin / admin123)")
print("   Site:        http://127.0.0.1:8000/")
