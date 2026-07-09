import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fooddelivery.settings")
django.setup()

from accounts.models import User
from restaurants.models import Category, Restaurant
from menu.models import MenuCategory, MenuItem

admin = User.objects.get(username="admin")

# ── Categories ──────────────────────────────────────────────
cat_data = [
    ("Pizza","🍕"),("Burgers","🍔"),("Chinese","🍜"),("Indian","🍛"),
    ("Biryani","🍚"),("Desserts","🍰"),("Sushi","🍣"),("Salads","🥗"),
    ("Italian","🍝"),("Mexican","��"),
]
cats = {}
for name, icon in cat_data:
    obj, _ = Category.objects.get_or_create(name=name, defaults={"icon": icon})
    cats[name] = obj

# ── Menu Categories ──────────────────────────────────────────
mcat_names = ["Starters","Main Course","Beverages","Desserts","Sides","Breads","Rolls"]
mc = {}
for name in mcat_names:
    obj, _ = MenuCategory.objects.get_or_create(name=name)
    mc[name] = obj

S  = mc["Starters"]
M  = mc["Main Course"]
B  = mc["Beverages"]
D  = mc["Desserts"]
Si = mc["Sides"]
Br = mc["Breads"]

def add_items(restaurant, items):
    for cat, name, desc, price, veg, vegan, spicy in items:
        if not MenuItem.objects.filter(restaurant=restaurant, name=name).exists():
            MenuItem.objects.create(
                restaurant=restaurant, category=cat, name=name,
                description=desc, price=price,
                is_vegetarian=veg, is_vegan=vegan, is_spicy=spicy
            )

# ── 1. Burger Nation ─────────────────────────────────────────
if not Restaurant.objects.filter(name="Burger Nation").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Burger Nation",
        description="Juicy handcrafted burgers made fresh daily with premium ingredients.",
        address="5 Park Street", city="Mumbai", phone="9123456780",
        email="burgernation@food.com", category=cats["Burgers"],
        delivery_time=25, minimum_order=100, delivery_charge=20, rating=4.3
    )
    add_items(r, [
        (S,  "Crispy Chicken Wings",   "Deep fried wings with hot sauce",              149, False, False, True),
        (S,  "Loaded Nachos",          "Tortilla chips with cheese and jalapenos",     129, True,  False, True),
        (M,  "Classic Beef Burger",    "Juicy beef patty with lettuce and cheese",     199, False, False, False),
        (M,  "Veg Burger",             "Crispy veggie patty with fresh veggies",       149, True,  False, False),
        (M,  "Double Smash Burger",    "Double beef patty with special sauce",         279, False, False, False),
        (M,  "BBQ Bacon Burger",       "Smoky bacon with BBQ sauce",                   249, False, False, False),
        (M,  "Mushroom Swiss Burger",  "Sauteed mushrooms with Swiss cheese",          219, True,  False, False),
        (Si, "French Fries",           "Golden crispy fries",                           79, True,  True,  False),
        (Si, "Onion Rings",            "Crispy battered onion rings",                   89, True,  True,  False),
        (B,  "Chocolate Milkshake",    "Thick creamy chocolate shake",                 119, True,  False, False),
        (B,  "Strawberry Lemonade",    "Fresh strawberry lemonade",                     89, True,  True,  False),
        (D,  "Brownie Sundae",         "Warm brownie with vanilla ice cream",           149, True,  False, False),
    ])
    print("Created: Burger Nation (12 items)")

# ── 2. Pizza Palace ──────────────────────────────────────────
if not Restaurant.objects.filter(name="Pizza Palace").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Pizza Palace",
        description="Wood-fired authentic Italian pizzas with fresh toppings and hand-tossed dough.",
        address="22 Brigade Road", city="Bangalore", phone="9234567891",
        email="pizzapalace@food.com", category=cats["Pizza"],
        delivery_time=30, minimum_order=200, delivery_charge=25, rating=4.5
    )
    add_items(r, [
        (M, "Margherita Pizza",      "Classic tomato sauce with mozzarella and basil",    249, True,  False, False),
        (M, "Pepperoni Pizza",       "Loaded with spicy pepperoni slices",                329, False, False, True),
        (M, "BBQ Chicken Pizza",     "Grilled chicken with BBQ sauce and onions",         349, False, False, False),
        (M, "Veggie Supreme",        "Bell peppers, olives, mushrooms and corn",          299, True,  False, False),
        (M, "Paneer Tikka Pizza",    "Indian fusion with spiced paneer",                  319, True,  False, True),
        (M, "Four Cheese Pizza",     "Mozzarella, cheddar, parmesan and gouda",           369, True,  False, False),
        (S, "Garlic Bread",          "Toasted bread with garlic butter",                   99, True,  False, False),
        (S, "Bruschetta",            "Tomato and basil on toasted bread",                 119, True,  False, False),
        (M, "Pasta Arrabbiata",      "Penne in spicy tomato sauce",                       199, True,  False, True),
        (D, "Tiramisu",              "Classic Italian coffee dessert",                    179, True,  False, False),
        (B, "Coke",                  "Chilled Coca-Cola 300ml",                            49, True,  True,  False),
        (B, "Fresh Lime Soda",       "Refreshing lime with soda",                          59, True,  True,  False),
    ])
    print("Created: Pizza Palace (12 items)")

# ── 3. Dragon Wok ────────────────────────────────────────────
if not Restaurant.objects.filter(name="Dragon Wok").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Dragon Wok",
        description="Authentic Chinese cuisine with wok-tossed dishes and traditional recipes.",
        address="8 Nehru Place", city="Delhi", phone="9345678902",
        email="dragonwok@food.com", category=cats["Chinese"],
        delivery_time=40, minimum_order=150, delivery_charge=30, rating=4.2
    )
    add_items(r, [
        (S,  "Spring Rolls",         "Crispy vegetable spring rolls with sweet chili sauce", 99,  True,  False, False),
        (S,  "Chicken Dumplings",    "Steamed dumplings with ginger soy dip",                149, False, False, False),
        (S,  "Veg Manchurian",       "Fried veggie balls in spicy manchurian sauce",         129, True,  False, True),
        (M,  "Chicken Fried Rice",   "Wok-tossed rice with egg and chicken",                 199, False, False, False),
        (M,  "Veg Fried Rice",       "Wok-tossed rice with mixed vegetables",                169, True,  False, False),
        (M,  "Kung Pao Chicken",     "Spicy stir-fried chicken with peanuts",                249, False, False, True),
        (M,  "Chilli Paneer",        "Crispy paneer in spicy chilli sauce",                  219, True,  False, True),
        (M,  "Hakka Noodles",        "Stir-fried noodles with vegetables",                   179, True,  False, False),
        (M,  "Sweet and Sour Pork",  "Tender pork in tangy sweet sour sauce",                269, False, False, False),
        (M,  "Tofu Stir Fry",        "Silken tofu with bok choy and soy",                    189, True,  True,  False),
        (Si, "Steamed Rice",         "Plain steamed jasmine rice",                            59, True,  True,  False),
        (B,  "Green Tea",            "Hot brewed Chinese green tea",                          49, True,  True,  False),
        (B,  "Lychee Juice",         "Chilled lychee fruit juice",                            79, True,  True,  False),
        (D,  "Mango Pudding",        "Silky smooth mango pudding",                            99, True,  False, False),
    ])
    print("Created: Dragon Wok (14 items)")

# ── 4. Biryani House ─────────────────────────────────────────
if not Restaurant.objects.filter(name="Biryani House").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Biryani House",
        description="Slow-cooked dum biryani with secret spice blends passed down generations.",
        address="45 Banjara Hills", city="Hyderabad", phone="9456789013",
        email="biryanihouse@food.com", category=cats["Biryani"],
        delivery_time=45, minimum_order=200, delivery_charge=0, rating=4.7
    )
    add_items(r, [
        (M,  "Hyderabadi Chicken Biryani", "Aromatic basmati rice with tender chicken",    299, False, False, True),
        (M,  "Mutton Biryani",             "Slow-cooked mutton with saffron rice",          379, False, False, True),
        (M,  "Veg Biryani",                "Fragrant rice with seasonal vegetables",        229, True,  False, False),
        (M,  "Egg Biryani",                "Biryani with boiled eggs and spices",           249, False, False, False),
        (M,  "Prawn Biryani",              "Juicy prawns with aromatic basmati",            349, False, False, True),
        (S,  "Mirchi Ka Salan",            "Spicy green chilli curry",                       99, True,  False, True),
        (S,  "Raita",                      "Cooling yogurt with cucumber and mint",          59, True,  False, False),
        (S,  "Chicken 65",                 "Crispy spiced fried chicken",                   179, False, False, True),
        (S,  "Seekh Kebab",                "Minced lamb kebabs on skewers",                 199, False, False, True),
        (Br, "Sheermal",                   "Sweet saffron flatbread",                        49, True,  False, False),
        (B,  "Lassi",                      "Chilled sweet yogurt drink",                     69, True,  False, False),
        (B,  "Rooh Afza Sharbat",          "Rose flavoured chilled drink",                   59, True,  False, False),
        (D,  "Double Ka Meetha",           "Hyderabadi bread pudding with rabri",           129, True,  False, False),
        (D,  "Qubani Ka Meetha",           "Apricot dessert with cream",                    119, True,  False, False),
    ])
    print("Created: Biryani House (14 items)")

# ── 5. The Curry Leaf ────────────────────────────────────────
if not Restaurant.objects.filter(name="The Curry Leaf").exists():
    r = Restaurant.objects.create(
        owner=admin, name="The Curry Leaf",
        description="South Indian comfort food - dosas, idlis and curries made with love.",
        address="7 Anna Salai", city="Chennai", phone="9567890124",
        email="curryleaf@food.com", category=cats["Indian"],
        delivery_time=30, minimum_order=100, delivery_charge=15, rating=4.4
    )
    add_items(r, [
        (S,  "Masala Dosa",           "Crispy dosa with spiced potato filling",          129, True,  False, False),
        (S,  "Idli Sambar",           "Soft steamed rice cakes with lentil soup",         99, True,  False, False),
        (S,  "Medu Vada",             "Crispy lentil doughnuts with coconut chutney",     89, True,  False, False),
        (S,  "Uttapam",               "Thick rice pancake with onion and tomato",        119, True,  False, False),
        (M,  "Chettinad Chicken",     "Fiery chicken curry with whole spices",           249, False, False, True),
        (M,  "Sambar Rice",           "Rice mixed with tangy lentil sambar",             149, True,  False, False),
        (M,  "Rasam Rice",            "Rice with peppery tomato rasam",                  129, True,  False, True),
        (M,  "Prawn Masala",          "Spicy coastal prawn curry",                       279, False, False, True),
        (M,  "Vegetable Kootu",       "Mixed vegetables in coconut gravy",               169, True,  True,  False),
        (Si, "Coconut Chutney",       "Fresh ground coconut chutney",                     39, True,  True,  False),
        (B,  "Filter Coffee",         "Strong South Indian drip coffee",                  49, True,  False, False),
        (B,  "Buttermilk",            "Spiced chilled buttermilk",                        39, True,  False, False),
        (D,  "Payasam",               "Sweet vermicelli pudding with cardamom",           89, True,  False, False),
    ])
    print("Created: The Curry Leaf (13 items)")

# ── 6. Sweet Tooth Bakery ────────────────────────────────────
if not Restaurant.objects.filter(name="Sweet Tooth Bakery").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Sweet Tooth Bakery",
        description="Freshly baked cakes, pastries and desserts made with the finest ingredients.",
        address="3 Linking Road", city="Mumbai", phone="9678901235",
        email="sweettooth@food.com", category=cats["Desserts"],
        delivery_time=20, minimum_order=150, delivery_charge=20, rating=4.6
    )
    add_items(r, [
        (D, "Chocolate Truffle Cake", "Rich dark chocolate cake with ganache",           349, True, False, False),
        (D, "Red Velvet Cake",        "Classic red velvet with cream cheese frosting",   329, True, False, False),
        (D, "Blueberry Cheesecake",   "Creamy cheesecake with blueberry compote",        299, True, False, False),
        (D, "Tiramisu",               "Italian coffee dessert with mascarpone",          279, True, False, False),
        (D, "Gulab Jamun",            "Soft milk dumplings in rose sugar syrup",          99, True, False, False),
        (D, "Rasgulla",               "Spongy cottage cheese balls in syrup",             89, True, False, False),
        (D, "Brownie",                "Fudgy dark chocolate brownie",                    129, True, False, False),
        (D, "Creme Brulee",           "Classic French vanilla custard",                  199, True, False, False),
        (S, "Croissant",              "Buttery flaky French pastry",                      89, True, False, False),
        (S, "Blueberry Muffin",       "Freshly baked blueberry muffin",                   79, True, False, False),
        (S, "Cinnamon Roll",          "Warm cinnamon roll with icing",                    99, True, False, False),
        (B, "Hot Chocolate",          "Rich creamy hot chocolate",                        99, True, False, False),
        (B, "Cappuccino",             "Espresso with steamed milk foam",                  89, True, False, False),
        (B, "Mango Smoothie",         "Fresh mango blended with yogurt",                 119, True, False, False),
    ])
    print("Created: Sweet Tooth Bakery (14 items)")

# ── 7. Sushi Zen ─────────────────────────────────────────────
if not Restaurant.objects.filter(name="Sushi Zen").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Sushi Zen",
        description="Premium Japanese sushi and sashimi crafted by expert chefs using fresh ingredients.",
        address="14 Juhu Beach Road", city="Mumbai", phone="9789012346",
        email="sushizen@food.com", category=cats["Sushi"],
        delivery_time=35, minimum_order=300, delivery_charge=40, rating=4.8
    )
    add_items(r, [
        (S,  "Edamame",              "Steamed salted soybean pods",                      99, True,  True,  False),
        (S,  "Miso Soup",            "Traditional Japanese miso with tofu",              79, True,  False, False),
        (S,  "Gyoza",                "Pan-fried pork and cabbage dumplings",            149, False, False, False),
        (M,  "Salmon Nigiri",        "Fresh salmon over seasoned rice",                 249, False, False, False),
        (M,  "Tuna Sashimi",         "Premium sliced raw tuna",                         299, False, False, False),
        (M,  "California Roll",      "Crab, avocado and cucumber maki roll",            229, False, False, False),
        (M,  "Spicy Tuna Roll",      "Tuna with spicy mayo in nori roll",               269, False, False, True),
        (M,  "Veggie Roll",          "Avocado, cucumber and carrot roll",               199, True,  False, False),
        (M,  "Dragon Roll",          "Shrimp tempura topped with avocado",              349, False, False, False),
        (M,  "Ramen",                "Rich tonkotsu broth with noodles and pork",       299, False, False, False),
        (Si, "Pickled Ginger",       "Thinly sliced pickled ginger",                     39, True,  True,  False),
        (B,  "Sake",                 "Traditional Japanese rice wine",                  199, True,  False, False),
        (B,  "Matcha Latte",         "Creamy hot matcha green tea latte",               129, True,  False, False),
        (D,  "Mochi Ice Cream",      "Japanese rice cake with ice cream filling",       149, True,  False, False),
    ])
    print("Created: Sushi Zen (14 items)")

# ── 8. Taco Fiesta ───────────────────────────────────────────
if not Restaurant.objects.filter(name="Taco Fiesta").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Taco Fiesta",
        description="Vibrant Mexican street food with bold flavours, fresh salsas and loaded tacos.",
        address="9 Connaught Place", city="Delhi", phone="9890123457",
        email="tacofiesta@food.com", category=cats["Mexican"],
        delivery_time=25, minimum_order=150, delivery_charge=20, rating=4.3
    )
    add_items(r, [
        (S,  "Nachos with Salsa",    "Tortilla chips with fresh tomato salsa",          119, True,  False, False),
        (S,  "Guacamole",            "Fresh avocado dip with lime and cilantro",        129, True,  True,  False),
        (S,  "Quesadilla",           "Grilled tortilla with cheese and peppers",        149, True,  False, False),
        (M,  "Chicken Tacos",        "Spiced chicken in soft corn tortillas",           199, False, False, True),
        (M,  "Beef Burrito",         "Flour tortilla stuffed with beef and rice",       249, False, False, True),
        (M,  "Veg Burrito",          "Beans, rice and veggies in a flour tortilla",     199, True,  False, False),
        (M,  "Chicken Enchiladas",   "Rolled tortillas in spicy red sauce",             229, False, False, True),
        (M,  "Fish Tacos",           "Crispy fish with cabbage slaw and lime",          219, False, False, False),
        (M,  "Veg Fajitas",          "Sizzling peppers and onions with tortillas",      189, True,  False, False),
        (Si, "Mexican Rice",         "Tomato-flavoured seasoned rice",                   79, True,  True,  False),
        (Si, "Refried Beans",        "Creamy seasoned pinto beans",                      69, True,  False, False),
        (B,  "Horchata",             "Sweet cinnamon rice milk drink",                   89, True,  False, False),
        (B,  "Agua Fresca",          "Fresh fruit water with lime",                      69, True,  True,  False),
        (D,  "Churros",              "Fried dough sticks with chocolate dip",           129, True,  False, False),
    ])
    print("Created: Taco Fiesta (14 items)")

# ── 9. Green Bowl ────────────────────────────────────────────
if not Restaurant.objects.filter(name="Green Bowl").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Green Bowl",
        description="Healthy salads, grain bowls and smoothies for the health-conscious foodie.",
        address="18 Koregaon Park", city="Pune", phone="9901234568",
        email="greenbowl@food.com", category=cats["Salads"],
        delivery_time=20, minimum_order=200, delivery_charge=30, rating=4.5
    )
    add_items(r, [
        (M,  "Caesar Salad",         "Romaine, croutons, parmesan with caesar dressing",  179, True,  False, False),
        (M,  "Greek Salad",          "Cucumber, olives, feta and tomatoes",               169, True,  False, False),
        (M,  "Quinoa Power Bowl",    "Quinoa with roasted veggies and tahini",             249, True,  True,  False),
        (M,  "Grilled Chicken Bowl", "Grilled chicken with brown rice and greens",         279, False, False, False),
        (M,  "Avocado Toast Bowl",   "Smashed avocado on multigrain with eggs",            229, True,  False, False),
        (M,  "Buddha Bowl",          "Chickpeas, sweet potato, kale and hummus",           239, True,  True,  False),
        (M,  "Tuna Nicoise",         "Tuna, green beans, eggs and olives",                 259, False, False, False),
        (S,  "Hummus Platter",       "Creamy hummus with pita and veggies",                149, True,  True,  False),
        (S,  "Fruit Bowl",           "Seasonal fresh cut fruits",                          129, True,  True,  False),
        (B,  "Green Detox Juice",    "Spinach, cucumber, apple and ginger",                119, True,  True,  False),
        (B,  "Berry Smoothie",       "Mixed berries blended with almond milk",             139, True,  True,  False),
        (B,  "Coconut Water",        "Fresh tender coconut water",                          69, True,  True,  False),
        (D,  "Chia Pudding",         "Chia seeds in coconut milk with mango",              149, True,  True,  False),
    ])
    print("Created: Green Bowl (13 items)")

# ── 10. Royal Tandoor ────────────────────────────────────────
if not Restaurant.objects.filter(name="Royal Tandoor").exists():
    r = Restaurant.objects.create(
        owner=admin, name="Royal Tandoor",
        description="Mughlai and North Indian cuisine with rich gravies, kebabs and tandoor specialties.",
        address="33 Civil Lines", city="Lucknow", phone="9012345679",
        email="royaltandoor@food.com", category=cats["Indian"],
        delivery_time=40, minimum_order=250, delivery_charge=35, rating=4.6
    )
    add_items(r, [
        (S,  "Galouti Kebab",        "Melt-in-mouth minced lamb kebabs",                  249, False, False, False),
        (S,  "Paneer Tikka",         "Grilled cottage cheese with spiced marinade",        199, True,  False, True),
        (S,  "Chicken Tikka",        "Tender chicken marinated in yogurt and spices",      229, False, False, True),
        (S,  "Hara Bhara Kebab",     "Spinach and pea patties with mint chutney",          149, True,  False, False),
        (M,  "Butter Chicken",       "Creamy tomato-based chicken curry",                  299, False, False, False),
        (M,  "Dal Makhani",          "Slow-cooked black lentils in butter and cream",      219, True,  False, False),
        (M,  "Rogan Josh",           "Aromatic Kashmiri lamb curry",                       349, False, False, True),
        (M,  "Palak Paneer",         "Cottage cheese in creamy spinach gravy",             239, True,  False, False),
        (M,  "Chicken Korma",        "Mild chicken curry with cashew and cream",           279, False, False, False),
        (M,  "Shahi Paneer",         "Paneer in rich Mughlai gravy",                       259, True,  False, False),
        (Br, "Butter Naan",          "Soft leavened bread with butter",                     49, True,  False, False),
        (Br, "Garlic Naan",          "Naan topped with garlic and coriander",               59, True,  False, False),
        (Br, "Tandoori Roti",        "Whole wheat bread from clay oven",                    39, True,  False, False),
        (B,  "Mango Lassi",          "Chilled mango yogurt drink",                          89, True,  False, False),
        (B,  "Masala Chai",          "Spiced Indian tea with milk",                         49, True,  False, False),
        (D,  "Gulab Jamun",          "Soft milk dumplings in rose sugar syrup",             99, True,  False, False),
        (D,  "Kulfi",                "Traditional Indian ice cream with pistachio",         89, True,  False, False),
    ])
    print("Created: Royal Tandoor (17 items)")

print("")
print("=" * 50)
print("Seed complete!")
print(f"Total restaurants : {Restaurant.objects.count()}")
print(f"Total menu items  : {MenuItem.objects.count()}")
print("=" * 50)
