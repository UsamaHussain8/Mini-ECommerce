from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from Products.models import Product

def add_item_to_cart(request, slug):
    product = Product.objects.prefetch_related('tags').get(slug = slug)
    current_user = request.user

    cart, is_created = Cart.objects.get_or_create(store_user = current_user.storeuser)
    cart.save()

    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

@login_required(login_url = "login_view")
def display_cart(request):
    cart = Cart.objects.get(store_user = request.user.storeuser)
    cart_item = list(CartItem.objects.filter(cart = cart))
    total_price = cart.calculate_total_price()
    return render(request, "Cart/cart_details.html", context={"items": cart_item, "price": total_price})
