from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.shortcuts import redirect, render
from django.utils import html
from django.views import View

# Create your views here.
def simple(request):
    return render(request,'templatee/simple.html')

class GuessView(View):
    def get(self,request): # get request
        # post redirect get refresh
        # mutiple post in refresh
        return render(request,'templatee/guess.html',{'zap':None})

    def post(self,request): # post request
        guess = request.POST.get('guess')
        msg = checkguess(guess)
        return render(request,'templatee/guess.html',{'zap':msg})

def checkguess(guess):
    msg = False
    if guess:
        try:
            if int(guess)<42:
                msg = "Guess too low"
            elif int(guess)>42:
                msg = "Guess too high"
            else:
                msg = "Right"
        except:
            msg = 'Bad format for guess'+html.escape(guess)
    return msg

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

class http_response(View):
    def get(self,request):
        response  = 'This is a http response text'
        return HttpResponse(response)
class url_get(View):
    def get(self,request) :
        response = """<html><body>
        <p>Your guess was """+escape(request.GET['guess'])+"""</p>
        </body></html>"""
        return HttpResponse(response)

class url_redirect(View):
    def get(self,request):
        return HttpResponseRedirect('https://www.google.com')