from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import JsonResponse, HttpResponse
from chat.models import Room,Message
from django.contrib.auth.models import User
import time

class HomeView(View) :
    def get(self, request):
        return render(request, 'chat/main.html')

@login_required(login_url='/accounts/login')
def room(request, room):
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'room': room,
        'room_details': room_details
    })

@login_required(login_url='/accounts/login')
def checkroom(request):
    room = request.POST['room_name']
    print(request.POST)
    if Room.objects.filter(name=room).exists():
        return redirect('/chat/'+room)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/chat/'+room)
    
@login_required(login_url='/accounts/login')
def send(request):
    message = request.POST['message']
    username = request.user
    rooms = request.POST['room_name']
    room_details = Room.objects.get(name=rooms)

    new_message = Message.objects.create(text=message, owner=username, room=room_details)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required(login_url='/accounts/login')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    user_list = list(User.objects.all())
    list_user=[str(user) for user in user_list]
   
    messages = Message.objects.filter(room=room_details.id)
   
    return JsonResponse({"messages":list(messages.values()),"user_list":list_user})

def jsonfun(request):
    time.sleep(2)
    stuff = {
        'first': 'first thing',
        'second': 'second thing'
    }
    return JsonResponse(stuff)

class TalkMain(LoginRequiredMixin, View) :
    def get(self, request):
        return render(request, 'chat/talk.html')

    def post(self, request) :
        message = Message(text=request.POST['message'], owner=request.user)
        message.save()
        return redirect(reverse('chat:talk'))

class TalkMessages(LoginRequiredMixin, View) :
    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')[:10]
        results = []
        for message in messages:
            result = [message.text, naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe=False)


# References

# https://simpleisbetterthancomplex.com/tutorial/2016/07/27/how-to-return-json-encoded-response.html
