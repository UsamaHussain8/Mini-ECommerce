from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Tag, Product

@login_required(login_url="login_view")
def list_products(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'Products/list_products.html', context=context)

@login_required(login_url="login_view")
def product_details(request, slug):
    product_inspected = Product.objects.get(slug=slug)
    context = {"product": product_inspected}
    return render(request, 'Products/product_details.html', context)

@login_required(login_url="login_view")
class ProductListView(ListView):
    model = Product
    paginate_by = 10 
    template_name = "list_products.html"
    context_object_name = "products"

    
