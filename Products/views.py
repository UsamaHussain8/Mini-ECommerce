from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from Reviews.forms import ReviewForm
from Reviews.models import Review
from .models import Tag, Product

def list_products(request):
    products = Product.objects.all()
    #context = {"products": products}
    return render(request, 'Products/products.html', {'segment': 'products', "products": products})

def product_details(request, slug):
    product_inspected = Product.objects.get(slug=slug)
    context = {"product": product_inspected}
    return render(request, 'Products/product.html', {'segment': 'products', "product": product_inspected})

def all_product_categories(request, category):
    tags = Tag.objects.all()
    return render(request, 'core/index.html', {'segment': 'products', "tags": tags})

def product_categories(request, tag):
    tag_obj=Tag.objects.get(caption=tag)
    products = Product.objects.filter(tags=tag_obj)
    return render(request, 'Products/products.html', {'segment': 'products', "products": products})

class ProductListView(ListView):
    model = Product
    paginate_by = 10 
    template_name = "Products/products.html"
    context_object_name = "products"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        product_list = context['products']
        tags_list = [product.tags.all() for product in product_list]
        context['tags'] = tags_list
        context['segment'] = 'products'
        context['search_query'] = self.request.GET.get('search_products', '')

        return context
    
class ProductsSearchView(ListView):
    model = Product
    template_name = "Products/products.html"
    context_object_name = "searched_products"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        product_list = context['searched_products']
        tags_list = Tag.objects.all()
        context['tags'] = tags_list
        context['segment'] = 'products'
        context['search_query'] = self.request.GET.get('search_products', '')

        return context
    
    def get_queryset(self):
        search_query = self.request.GET.get('search_products')
        queryset = Product.objects.prefetch_related('tags').all()
        if search_query:
            return queryset.filter(name__icontains=search_query)
        return queryset
    
class ReviewFormView(LoginRequiredMixin, FormView):
    template_name = "Product/product.html"
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save()
        return super().form_valid(form)