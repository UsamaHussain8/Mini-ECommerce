from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from Reviews.forms import ReviewForm
from Reviews.models import Review
from .models import Tag, Product

@login_required(login_url="login_view")
def list_products(request):
    products = Product.objects.all()
    #context = {"products": products}
    return render(request, 'Products/products.html', {'segment': 'products', "products": products})

@login_required(login_url="login_view")
def product_details(request, slug):
    product_inspected = Product.objects.get(slug=slug)
    context = {"product": product_inspected}
    return render(request, 'Products/product.html', context)

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 10 
    template_name = "Products/products.html"
    context_object_name = "products"
    segment = "products"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        product_list = context['products']
        tags_list = [product.tags.all() for product in product_list]
        context['tags'] = tags_list
        
        return context
    
class ReviewFormView(LoginRequiredMixin, FormView):
    template_name = "Product/product.html"
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save()
        return super().form_valid(form)