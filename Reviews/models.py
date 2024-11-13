from django.db import models
from core.models import StoreUser as AUTH_USER
from Products.models import Product

class Review(models.Model):
    review = models.TextField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review}'