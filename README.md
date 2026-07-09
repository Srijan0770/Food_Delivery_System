# 🍔 FoodExpress — Online Food Delivery System

A full-featured Django web application for online food ordering and delivery.

## Features

- **Customer** — Browse restaurants, search by category/city, add to cart, place orders, track status, leave reviews
- **Restaurant Owner** — Manage restaurants, full menu CRUD, view & update incoming orders
- **Admin** — Full Django admin panel for all models

## Tech Stack

- Django 6.0 + SQLite
- Bootstrap 5.3 (CDN)
- Pillow (image uploads)

## Quick Start

```bash
# 1. Install dependencies
pip install django pillow

# 2. Apply migrations
python manage.py migrate

# 3. Seed sample data & create admin
python create_superuser.py

# 4. Run the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/ → `admin` / `admin123`

## Project Structure

```
├── accounts/       # Custom user model, auth (register/login/profile)
├── restaurants/    # Restaurant listings, categories, reviews
├── menu/           # Menu items management
├── cart/           # Session-based cart
├── orders/         # Checkout, order tracking, status management
├── fooddelivery/   # Project settings & root URLs
├── templates/      # All HTML templates
└── static/         # CSS & JS
```

## User Roles

| Role | Capabilities |
|------|-------------|
| Customer | Browse, order, review |
| Restaurant Owner | Manage restaurant + menu + orders |
| Delivery Agent | (extendable) |
