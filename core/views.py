from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserSignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from allauth.socialaccount.models import SocialAccount

def index(request):
    return render(request, "core/index.html")

def contacts(request):
    return render(request, "core/contacts.html")

def create_user(request):
    if request.method == "POST":
        user_form = UserSignUpForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, f"Thanks for singing up: {user.username}")
            # login(request, user)
            return redirect('login_view')
        else:
            messages.error(request, 'Some error occured')

    else:
        user_form = UserSignUpForm()
    
    return render(request, 'core/signup.html', context= {"form": user_form})

def register(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f"New account created: {username}")
      login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      print(user)
    else:
      messages.error(request, "Account creation failed")

    return redirect("welcome")

  form = UserCreationForm()
  return render(request, "core/signup.html", {"form": form})

def get_profile_picture(user):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='facebook')
        return social_account.extra_data.get('picture', {}).get('data', {}).get('url')
    except SocialAccount.DoesNotExist:
        return None