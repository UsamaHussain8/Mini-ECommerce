from django.db import models
from django.contrib.auth.models import User
from core.models import StoreUser
from Products.models import Product
from django.core.exceptions import ValidationError

class Cart(models.Model):
    store_user = models.OneToOneField(StoreUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.store_user.user.username} has a cart worth {self.total_amount}'
    
    def calculate_total_price(self):
        cart_items = self.cartitem_set.all()  # Get all cart items associated with the cart
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return total_price
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product} with {self.quantity} number of items'

    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError(f"Only {self.product.quantity} items available in stock.")
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is applied
        super().save(*args, **kwargs)