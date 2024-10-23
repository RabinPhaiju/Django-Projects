# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import LoginForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('homepage')  # Redirect to a home page or wherever you'd like
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            else:
                return redirect('homepage')
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('homepage')

def homepage(request):
    return render(request, 'homepage.html')