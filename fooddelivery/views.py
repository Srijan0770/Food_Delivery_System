from django.shortcuts import render
from restaurants.models import Restaurant, Category


def home(request):
    featured_restaurants = Restaurant.objects.filter(is_active=True).order_by('-rating')[:6]
    categories = Category.objects.all()
    context = {
        'featured_restaurants': featured_restaurants,
        'categories': categories,
    }
    return render(request, 'home.html', context)
