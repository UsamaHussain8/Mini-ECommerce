from django.db import models
from django.contrib.auth.models import User
from Products.models import Product

class Seller(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)