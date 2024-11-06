from django.urls import path
from . import views
from .views import ProductListView

urlpatterns = [
    path('list_products', ProductListView.as_view(), name = "list_products_view"),
    path('product_details/<slug:slug>', views.product_details, name="product_details"),
    path('product_details/<slug:slug>', views.ReviewFormView.as_view(), name="product_review"),
]
