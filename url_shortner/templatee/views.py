from django.shortcuts import redirect, render
from django.views.generic import View

# Create your views here.
def simple(request):
    return render(request,'templatee/simple.html')


def guess(request):
    context = {'zap':'42'}
    return render(request,'templatee/guess.html',context)

def special(request):
    context = {
        'txt':'<b>bold text</b>',
        'zap':'42'
    }
    return render(request,'templatee/special.html',context)

def loop(request):
    fruits = ['Apple','Orange','Papaya']
    nuts = ['peanut','cashew']
    context = {'fruits':fruits,'nuts':nuts,'zap':'42'}

    return render(request,'templatee/loop.html',context)

def nested_object(request):
    x = {'outer':{'inner':'42'}}
    return render(request,'templatee/nested_object.html',x)

class GameView(View):
    def get(self,request,guess):
        x = {'guess':int(guess)}
        return render(request,'templatee/cond.html',x)