# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('polls:index')  # Redirect to a home page or wherever you'd like
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
