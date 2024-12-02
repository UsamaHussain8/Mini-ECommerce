from django.urls import path
from . import views
from .views import ProductListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list_products', ProductListView.as_view(), name = "products_list"),
    path('product_details/<slug:slug>', views.product_details, name="product_details"),
    path('product_details/<slug:slug>', views.ReviewFormView.as_view(), name="product_review"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)