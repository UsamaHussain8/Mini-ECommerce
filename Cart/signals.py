from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import CartItem
from Products.models import Product  # Import the Product model

@receiver(pre_save, sender=CartItem)
def adjust_product_quantity_on_save(sender, instance, **kwargs):
    """
    Adjust product quantity when a CartItem is saved.
    """
    # Get the current product
    product = instance.product

    if instance.pk:  # If the CartItem already exists (update case)
        # Get the previous state of the CartItem
        previous = CartItem.objects.get(pk=instance.pk)
        quantity_difference = instance.quantity - previous.quantity

        # Decrease product quantity if CartItem quantity increases
        if quantity_difference > 0:
            product.quantity -= quantity_difference
        # Increase product quantity if CartItem quantity decreases
        elif quantity_difference < 0:
            product.quantity += abs(quantity_difference)
    else:  # New CartItem (create case)
        product.quantity -= instance.quantity  # Decrease product quantity

    # Save the updated product
    product.save()

@receiver(post_delete, sender=CartItem)
def adjust_product_quantity_on_delete(sender, instance, **kwargs):
    """
    Increase product quantity when a CartItem is removed.
    """
    # Get the product and increase its quantity
    product = instance.product
    product.quantity += instance.quantity
    product.save()

@receiver(post_save, sender=CartItem)
def update_cart_total_amount(sender, instance, **kwargs):
    """
    Update the total amount of the cart when a CartItem is saved.
    """
    # Get the cart and update its total amount
    cart = instance.cart
    cart.total_amount = cart.calculate_total_price()
    cart.save()