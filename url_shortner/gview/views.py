from typing import List
from django.shortcuts import render
from django.views.generic import View
from django.views import generic
from gview.models import Cat,Dog,Horse,Car

# Create your views here.

class CatListView(View):
    model = Cat
    def get(self,request):
        modelname = self.model._meta.verbose_name.title().lower()
        stuff = self.model.objects.all()
        cntx = {modelname+'_list':stuff}
        return render(request,'gview/'+modelname+'_list.html',cntx)

# reuse the generic ListView. DRY
class DogListView(CatListView):
    model = Dog

class HorseListView(CatListView):
    model = Horse

class CarListView(CatListView):
    model = Car

class CatDetailView(View):
    model = Cat
    def get(self,request,pk):
        modelname = self.model._meta.verbose_name.title().lower()
        obj = self.model.objects.get(pk=pk)
        cntx = { modelname : obj }
        return render(request,'gview/'+modelname+'_detail.html',cntx)

class DogDetailView(CatDetailView):
    model = Dog

class HorseDetailView(CatDetailView):
    model = Horse

class CarDetailView(CatDetailView):
    model = Car