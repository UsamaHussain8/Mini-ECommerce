from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = "welcome"),
    path('contacts', views.contacts, name = "contacts"),
    path("register", views.register, name="create_user"),
    path('login', auth_views.LoginView.as_view(template_name="core/login.html"), name="login_view"),
    path('logout', auth_views.LogoutView.as_view(), name = "logout_view"),
    path('accounts/', include('allauth.urls')),
]
