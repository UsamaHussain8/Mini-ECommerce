from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_cart, name="cart"),
    path('add/<slug:slug>/', views.add_item_to_cart, name="add_cart_item"),
    path('api/cart/count/', views.count_cart_items, name="num_cart_items"),
    path('remove/<slug:slug>/', views.decrease_cart_item, name='decrease_items_from_cart'),
    path('discard/<slug:slug>/', views.remove_item_from_cart, name='remove_item_from_cart'),
]
