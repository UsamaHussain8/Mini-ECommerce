from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = "welcome"),
    path("register", views.register, name="create_user"),
    path('login', auth_views.LoginView.as_view(template_name="core/login.html"), name="login_view"),
    path('logout', auth_views.LogoutView.as_view(), name = "logout_view"),
    
]
