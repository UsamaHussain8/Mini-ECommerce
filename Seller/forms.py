from django.forms import ModelForm
from Products.models import Product
from .models import Seller

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ["slug"]