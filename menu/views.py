from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurants.models import Restaurant
from .models import MenuItem
from .forms import MenuItemForm


@login_required
def manage_menu(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'menu/manage.html', {'restaurant': restaurant, 'items': items})


@login_required
def add_menu_item(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk, owner=request.user)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            messages.success(request, 'Menu item added!')
            return redirect('manage_menu', restaurant_pk=restaurant_pk)
    else:
        form = MenuItemForm()
    return render(request, 'menu/form.html', {'form': form, 'restaurant': restaurant, 'title': 'Add Item'})


@login_required
def edit_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, restaurant__owner=request.user)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated!')
            return redirect('manage_menu', restaurant_pk=item.restaurant.pk)
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/form.html', {'form': form, 'restaurant': item.restaurant, 'title': 'Edit Item'})


@login_required
def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, restaurant__owner=request.user)
    restaurant_pk = item.restaurant.pk
    item.delete()
    messages.success(request, 'Menu item deleted.')
    return redirect('manage_menu', restaurant_pk=restaurant_pk)
