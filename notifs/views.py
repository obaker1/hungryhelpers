from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from notifications.signals import notify
from django.views.generic import DetailView


def index(request):
    # get list of users to present as options to send notifs to
    try:
        users = User.objects.all()
        print(request.user)
        user = User.objects.get(username=request.user)
        return render(request, 'index.html', {'users': users, 'user': user})
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages.")


def message(request):
    # get sender name, receiver name, and message to be sent
    try:
        if request.method == 'POST':
            sender = User.objects.get(username=request.user)
            receiver = User.objects.get(id=request.POST.get('user_id'))
            notify.send(sender, recipient=receiver, verb='Message', description=request.POST.get('message'))
            return redirect('index')
        else:
            return HttpResponse("Invalid request")
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages")

def inbox(request):
    return render(request, 'registration/inbox.html')
