from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Restaurant, Category, Review
from .forms import RestaurantForm, ReviewForm
from menu.models import MenuItem


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    categories = Category.objects.all()

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    city = request.GET.get('city', '')

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(city__icontains=query)
        )
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if city:
        restaurants = restaurants.filter(city__icontains=city)

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'city': city,
    }
    return render(request, 'restaurants/list.html', context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, is_active=True)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
    reviews = restaurant.reviews.select_related('user').order_by('-created_at')
    review_form = ReviewForm()

    # Group menu items by category
    menu_by_category = {}
    for item in menu_items:
        cat = item.category or 'Other'
        menu_by_category.setdefault(cat, []).append(item)

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    context = {
        'restaurant': restaurant,
        'menu_by_category': menu_by_category,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'avg_rating': restaurant.get_average_rating(),
    }
    return render(request, 'restaurants/detail.html', context)


@login_required
def add_review(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                restaurant=restaurant,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment'],
                }
            )
            messages.success(request, 'Review submitted successfully!')
    return redirect('restaurant_detail', pk=pk)


@login_required
def my_restaurant(request):
    if not request.user.is_restaurant_owner:
        messages.error(request, 'You need a restaurant owner account.')
        return redirect('home')
    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'restaurants/my_restaurant.html', {'restaurants': restaurants})


@login_required
def create_restaurant(request):
    if not request.user.is_restaurant_owner:
        messages.error(request, 'Only restaurant owners can create restaurants.')
        return redirect('home')
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(request, 'Restaurant created successfully!')
            return redirect('my_restaurant')
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/form.html', {'form': form, 'title': 'Add Restaurant'})


@login_required
def edit_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('my_restaurant')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'restaurants/form.html', {'form': form, 'title': 'Edit Restaurant'})
