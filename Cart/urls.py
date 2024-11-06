from django.urls import path
from . import views

urlpatterns = [
    path('add/<slug:slug>', views.add_item_to_cart, name="add_cart_item"),
    path('display_cart', views.display_cart, name = "display_cart")
]
