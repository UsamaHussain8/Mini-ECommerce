from django.shortcuts import render, redirect
from .models import Cart, CartItem
from Products.models import Product

def add_item_to_cart(request, slug):
    product = Product.objects.get(slug = slug)
    current_user = request.user

    cart, is_created = Cart.objects.get_or_create(user = current_user)
    cart.save()

    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("display_cart")

def display_cart(request):
    cart = Cart.objects.get(user = request.user)
    cart_item = list(CartItem.objects.filter(cart = cart))
    return render(request, "Cart/cart_details.html", context={"items": cart_item})
