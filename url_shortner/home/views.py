from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

# This is a little complex because we need to detect when we are
# running in various configurations


class HomeView(View):
    def get(self, request):
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }
        return render(request, 'home/home.html', context)

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login(request,user) # for direct login
            return redirect('')
        else:
            messages.error(request,'An error occur in registration.')

    return render(request,'registration/register.html',{'form':form})