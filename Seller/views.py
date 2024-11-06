from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from .models import Seller
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm

def index(request):
    return HttpResponse("<h3> Seller's Corner! </h3>")

def successful(request):
    return render(request, "Seller/successful.html")

class ProductFormView(LoginRequiredMixin, FormView):
    template_name = "Seller/add_product.html"
    form_class = ProductForm
    success_url = "thanks"

    def form_valid(self, form):
        # Save the form and the associated product
        product = form.save()
        return super().form_valid(form)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Seller
    template_name = "Seller/add_product.html"
    fields = ["product"]
    
