from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserSignUpForm
from .models import StoreUser
from django.contrib.auth import login, logout
from django.db import IntegrityError

# from django.conf import settings
# user = settings.AUTH_USER_MODEL

def index(request):
    return render(request, "core/index.html")

def contacts(request):
    return render(request, "core/contacts.html")

def register(request):
  if request.method == "POST":
    form = UserSignUpForm(request.POST)
    if form.is_valid():
      try:
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f"Thanks for signing up: {username}")
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      except IntegrityError:
         form.add_error('contact_number', "This contact number is already registered.")
    else:
      messages.error(request, "Account creation failed")
      return render(request, "core/signup.html", context={"form": form})

    return redirect("welcome")

  form = UserSignUpForm()
  return render(request, "core/signup.html", context={"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in as: {username}")
            return redirect('welcome')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, 'core/login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out")

    return redirect('login_view')

# def create_user(request):
#     if request.method == "POST":
#         user_form = UserSignUpForm(request.POST)

#         if user_form.is_valid():
#             user = user_form.save()
#             messages.success(request, f"Thanks for singing up: {user.username}")
#             # login(request, user)
#             return redirect('login_view')
#         else:
#             messages.error(request, 'Some error occured')

#     else:
#         user_form = UserSignUpForm()
    
#     return render(request, 'core/signup.html', context= {"form": user_form})
