from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .models import Review
from .forms import ReviewForm

def index(request):
    return HttpResponse("<h3> Reviews section </h3>")

class ReviewFormView(LoginRequiredMixin, FormView):
    template_name = "Product/product_details.html"
    form_class = ReviewForm

    def form_valid(self, form):
        # Save the form and the associated product
        review = form.save()
        return super().form_valid(form)
