from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.models import Cart


@login_required
def checkout(request):
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('restaurant_list')

    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('restaurant_list')

    restaurant = cart.restaurant
    subtotal = cart.get_total()
    delivery_charge = restaurant.delivery_charge if restaurant else 0
    total = subtotal + delivery_charge

    if subtotal < restaurant.minimum_order:
        messages.warning(
            request,
            f'Minimum order for {restaurant.name} is ₹{restaurant.minimum_order}. '
            f'Your cart total is ₹{subtotal}.'
        )
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.restaurant = restaurant
            order.subtotal = subtotal
            order.delivery_charge = delivery_charge
            order.total_amount = total
            order.save()

            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    item_name=cart_item.menu_item.name,
                    item_price=cart_item.menu_item.price,
                    quantity=cart_item.quantity,
                )

            cart.clear()
            messages.success(request, f'Order #{order.pk} placed successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = CheckoutForm(user=request.user)

    context = {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'total': total,
        'restaurant': restaurant,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).select_related('restaurant')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status in ('pending', 'confirmed'):
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.pk} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled at this stage.')
    return redirect('order_detail', pk=pk)


# --- Restaurant owner views ---
@login_required
def restaurant_orders(request):
    if not request.user.is_restaurant_owner:
        messages.error(request, 'Access denied.')
        return redirect('home')
    orders = Order.objects.filter(
        restaurant__owner=request.user
    ).select_related('user', 'restaurant')
    return render(request, 'orders/restaurant_orders.html', {'orders': orders})


@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk, restaurant__owner=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [s[0] for s in Order.STATUS_CHOICES]
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.pk} status updated to {order.get_status_display()}.')
    return redirect('restaurant_orders')
