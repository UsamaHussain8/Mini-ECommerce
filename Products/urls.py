from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('list_products', views.ProductListView.as_view(), name = "products_list"),
    path('searched_products', views.ProductsSearchView.as_view(), name = "searched_products_list"),
    path('product_categories/<str:tag>', views.product_categories, name="product_categories"),
    path('product_details/<slug:slug>', views.product_details, name="product_details"),
    path('api/get_price_ranges/', views.get_price_ranges, name='get_price_ranges'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)