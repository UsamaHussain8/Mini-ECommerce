from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="welcome_seller"),
    path("add", views.ProductFormView.as_view(), name="add_product"),
    path("thanks", views.successful, name="thanks")
]
