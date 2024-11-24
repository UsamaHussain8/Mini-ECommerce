from django.db import models
from Products.models import Product
from django.contrib.auth.models import User
class Review(models.Model):
    review = models.TextField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review}'