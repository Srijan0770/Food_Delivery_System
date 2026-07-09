from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from menu.models import MenuItem
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('menu_item').all()
    delivery_charge = cart.restaurant.delivery_charge if cart.restaurant else 0
    subtotal = cart.get_total()
    total = subtotal + delivery_charge
    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = get_or_create_cart(request.user)

    # If cart has items from a different restaurant, warn user
    if cart.restaurant and cart.restaurant != menu_item.restaurant:
        if request.POST.get('confirm') == 'yes':
            cart.clear()
        else:
            messages.warning(
                request,
                f'Your cart has items from {cart.restaurant.name}. '
                'Adding this item will clear your current cart. '
                'Confirm by clicking "Add" again.'
            )
            request.session['pending_item'] = item_id
            return redirect('restaurant_detail', pk=menu_item.restaurant.pk)

    cart.restaurant = menu_item.restaurant
    cart.save()

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'"{menu_item.name}" added to cart.')
    return redirect('restaurant_detail', pk=menu_item.restaurant.pk)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    if not request.user.cart.items.exists():
        request.user.cart.restaurant = None
        request.user.cart.save()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_detail')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart_detail')


@login_required
def clear_cart(request):
    cart = get_or_create_cart(request.user)
    cart.clear()
    messages.info(request, 'Cart cleared.')
    return redirect('cart_detail')
