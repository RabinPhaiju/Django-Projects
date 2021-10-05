from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.core import serializers
from django.contrib import messages
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.db import connection
from . models import URLData
from . forms import URLDataForm
from . forms import TestForm
from . serializers import URLDataSerializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import sqlite3
import string
import random

#Declare Key Varaibles
BASE_LIST='0123456789abcdefghijklmnopqrstuvwxyz./:'
BASE_DICT=dict((c,idx) for idx,c in enumerate(BASE_LIST))
service_url='http://localhost:8000'

class FullURLView(viewsets.ModelViewSet):
	queryset=URLData.objects.all()
	serializers_class=URLDataSerializers

def base_encode(integer, alphabet=BASE_LIST): #Convert ID to FullURL
    if integer == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while integer:
        integer, rem = divmod(integer, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def base_decode(request, reverse_base=BASE_DICT): #Convert Full URL to ID
    longurl=request
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(longurl[::-1]):
        ret += (length ** i) * reverse_base[c]
    return ret

def shortChars(): #Get Shortened URL endpoint
    SHORT_LIST_CHAR='0123456789'+string.ascii_letters
    return ''.join([random.choice(SHORT_LIST_CHAR) for i in range(10)])

def checkIDExists(ID): #Check to see if ID exists in DB
    sc=str(shortChars())
    Retreived_IDs=list(URLData.objects.values_list('URLID', flat=True))
    ##################### CURD in ORM ##############
    # URLData.objects.values() -> select all from table.
    # delete from table -> URLData.objects.filter(ShortURL='facebook.com').delete()
    # update from table -> URLData.objects.filter(ShortURL='facebook.com').update(ShortURL='messenger.com')
    # select as orderd -> URLData.objects.values.order_by('ShortURL')
    if str(ID) in Retreived_IDs:
        surl=URL_ID=URLData.objects.all().filter(URLID=str(ID))[0].ShortURL # getting filtered data.
        mess=("Record Already Exists. The Shortened Link is: {}/{}".format(service_url,surl))
    else:
        U=URLData(URLID=ID, ShortURL=sc)
        U.save() # add to database
        mess=("Congratulatons! Your shortened URL is {}/{}".format(service_url,sc))
    return mess

def redirect_short_url(request, short_url): #url
    redirect_url = service_url+'/shorten'
    try:
        URL_ID=URLData.objects.all().filter(ShortURL=short_url)[0].URLID
        redirect_url = base_encode(int(URL_ID))
    except Exception as e:
        print (e)
    return redirect(redirect_url)   

def appendPrefix(entry):
    match=['http','https']
    if any(x in entry for x in match):
        return entry
    else:
        return('https://'+str(entry))

def get_form(request): # url # convert to class so that we can add LoginRequiredMixin,
    if request.method=='POST':
        form=URLDataForm(request.POST)
        if form.is_valid():
            fullurl=form.cleaned_data['EnterURL']
            fullurladj=appendPrefix(fullurl)
            ID=base_decode(fullurladj.lower())
            messages.success(request, '{}'.format(checkIDExists(ID)))
    form=URLDataForm()
    return render(request, 'Shortner/form.html', {'form':form})

def get_cookie(request):
    resp = HttpResponse('<p>Setting cookies</p>')
    resp.set_cookie('zap',42) # no expired date | until browswer close
    resp.set_cookie('cake',2,max_age=1000) # seconds until expires
    if('zap' in request.COOKIES):
        resp = HttpResponse('<p> The cookie:zap value is '+request.COOKIES['zap']+'</p>')
    return resp

def get_session(request):
    num_visitors = request.session.get('num_visits',0)+1
    request.session['num_visits']=num_visitors
    if num_visitors > 4:
        del(request.session['num_visits'])
    
    return HttpResponse('view session counts='+str(num_visitors))

def test(request):
    return HttpResponse('<p>Test is a page test.</br> <a href="/testform/">Test Form</a></p>')

# Test form

def testform(request):
    if request.method=='POST':
        form=TestForm(request.POST)
        if form.is_valid():
            print('name: ',form.cleaned_data['name'])
        form = TestForm()
    else:
        old_data= {
            'name':"rabin",
            'age':26,
            'dob':'1995-02-09'
        }
        # form = TestForm(old_data)
        form = TestForm()
    ctx = {'form':form}
    return render(request,'Shortner/testform.html',ctx)