from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .forms import UserForm, StoreUserForm
from .models import StoreUser

def index(request):
    return render(request, "core/index.html", {'segment': 'home'})

def contacts(request):
    return render(request, "core/contacts.html", {'segment': 'contacts'})

@transaction.atomic
def register(request):
  if request.method == "POST":
    user_form = UserForm(request.POST)
    store_user_form = StoreUserForm(request.POST)
    
    if user_form.is_valid() and store_user_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data["password"])  # Ensure password is hashed
        user.save()
        
        store_user = store_user_form.save(commit=False)
        store_user.user = user
        store_user.contact_number = store_user_form.cleaned_data.get('contact_number')
        store_user.save()
           
        username = user_form.cleaned_data.get('username')
        messages.success(request, f"Thanks for signing up: {username}")
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      
        return redirect("welcome")
    else:
      messages.error(request, "Account creation failed")
      return render(request, "core/signup.html", context={"user_form": user_form, "store_user_form": store_user_form})

  user_form = UserForm()
  store_user_form = StoreUserForm()
  return render(request, "core/signup.html", context={"user_form": user_form, "store_user_form": store_user_form})

@login_required(login_url='login_view')
def profile(request, id):
    user = User.objects.select_related().filter(id=id).first()
    return render(request, "core/profile.html", context={"user": user})

def login_view(request):
  if request.method == "POST":
      username = request.POST.get('username')
      password = request.POST.get('password')
      print(f"{username}, {password}")
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
      print("Logged out")
      
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
