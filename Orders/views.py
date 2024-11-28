from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from core.models import StoreUser
from .models import Order, OrderItem 
from Cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_view')
@transaction.atomic
def checkout(request):
    user_store = request.user.storeuser
    cart = get_object_or_404(Cart, user=user_store)

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')  # Replace with your cart view URL name

    total_amount = cart.calculate_total_price()

    if request.method == "POST":
        # Capture shipping address and payment method from form or user profile
        shipping_address = user_store.address  # Or get from form
        payment_method = request.POST.get('payment_method', 'Credit Card') 

        # Create the Order
        order = Order.objects.create(
            user=user_store,
            cart=cart,
            total_amount=total_amount,
            shipping_address=shipping_address,
            payment_method=payment_method,
            status='PROCESSING'  
        )

        # Transfer CartItems to OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )

        #clear the cart
        cart_items.delete()
        messages.success(request, f"Order {order.id} has been placed successfully!")
        return redirect('order_detail', order_id=order.id) 

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'core/checkout.html', context)

