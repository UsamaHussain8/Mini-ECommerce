from django.urls import path
from . import views
from .views import ProductListView

urlpatterns = [
    path('list_products', views.list_products, name = "list_products_view"),
    path('product_details/<slug:slug>', views.product_details, name="product_details")
]
