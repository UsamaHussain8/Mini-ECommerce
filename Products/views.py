from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.db.models import Min, Max
from Reviews.forms import ReviewForm
from Reviews.models import Review
from .models import Tag, Product
import pdb

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
    search_query = request.GET.get('search_products')
    price_range = request.GET.get('price_range')
    tag_obj=Tag.objects.get(caption=tag)
    products = Product.objects.filter(tags=tag_obj)
    if search_query:
        products = products.filter(name__icontains=search_query)
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        products = products.filter(price__gte=min_price, price__lte=max_price)

    has_products = products.exists()

    return render(request, 'Products/products.html', 
                  {'segment': 'products', "products": products, "tag": tag, 
                   'selected_price_range': price_range, 'has_products': has_products})

# class ProductListView(ListView):
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
    
    def get_queryset(self):
        search_query = self.request.GET.get('search_products')
        price_range = self.request.GET.get('price_range')
        print(self.request.GET.get('tag', 'None'))
        queryset = Product.objects.prefetch_related('tags').all()
        if search_query:
            return queryset.filter(name__icontains=search_query)
        if price_range:
            min_price, max_price = map(int, price_range.split('-'))
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        return queryset
    
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
    
def get_price_ranges(request):
    tag = request.GET.get('tag')
    print(tag)
    if not tag:
        return JsonResponse({'error': 'No category selected'}, status=400)

    # Get min and max prices for the selected category
    prices = Product.objects.filter(tags__caption=tag).aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    min_price = prices['min_price']
    max_price = prices['max_price']

    # Handle case where there are no products in the category
    if min_price is None or max_price is None:
        return JsonResponse({'price_ranges': []})

    # Divide the price range into 4 equal parts
    step = (max_price - min_price) // 4
    price_ranges = [
        f"{min_price + i * step}-{min_price + (i + 1) * step - 1}"
        for i in range(4)
    ]

    # Ensure the last range includes the maximum price
    price_ranges[-1] = f"{min_price + 3 * step}-{max_price}"

    return JsonResponse({'price_ranges': price_ranges})

class ReviewFormView(LoginRequiredMixin, FormView):
    template_name = "Product/product.html"
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save()
        return super().form_valid(form)