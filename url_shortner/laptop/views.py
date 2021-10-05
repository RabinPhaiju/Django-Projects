from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from laptop.models import Laptop

# Create your views here.
class LaptopView(LoginRequiredMixin,View):
    def get(self,request): # get request
        lap = Laptop.objects.all()
        cntx = {'laptops':lap}
        return render(request,'laptop/laptop.html',cntx)

    def post(self,request): # post request
        pass