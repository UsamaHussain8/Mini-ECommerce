from django.db import models
from core.models import StoreUser
from Cart.models import Cart
from Products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('CASH_ON_DELIVERY', 'Cash_On_Deliery'),
        ('EASYPAISA', 'Easypaisa'),
        ('STRIPE', 'Stripe'),
    ]

    store_user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ordered_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='CASH_ON_DELIVERY')

    def __str__(self):
        return f'Order {self.id} by {self.store_user.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)  # Price of the product at the time of purchase

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'

