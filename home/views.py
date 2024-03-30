from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import *
from django.shortcuts import get_object_or_404

# Create your views here.

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request,'login.html')


def signuppage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        # lastname  = request.POST.get('last_name')
        # print(lastname)
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username or email already exists'})
        user = User.objects.create(email=email,username=username,password=make_password(password))
        user.save()
        return redirect('home')
    return render(request,'signup.html')

def createjoin(request):
    if request.method == 'POST':
        name = request.POST.get('roomName')
        chatroom,iscreated = ChatRoom.objects.get_or_create(name = name)
        # print(chatroom)
        if not chatroom.user.filter(pk=request.user.pk).exists():
            chatroom.user.add(request.user)
        else:
            print('already part of this!')
        return redirect(f'/chat/{name}')
    chatroom = ChatRoom.objects.filter(user=request.user)
    # chatroom = list(chatroom)
    # chatroom = chatroom.name
    # print(chatroom)
    chatroom = [str(cr.name) for cr in chatroom]
    template = {'chatroomnames': chatroom}
    return render(request,'createjoin.html',template)
def home(request):
    chatroom = ChatRoom.objects.filter(user=request.user)
    # chatroom = list(chatroom)
    # chatroom = chatroom.name
    # print(chatroom)
    chatroom = [str(cr.name) for cr in chatroom]
    template = {'chatroomnames':chatroom}
    return render(request,'home.html',template)


def chats(request,chat_room):
    chatroom = ChatRoom.objects.filter(name = chat_room)[0]
    # print(chatroom)
    messages = Messages.objects.filter(chatroom = chatroom)
    # print(messages)
    cr = ChatRoom.objects.filter(user=request.user)
    # chatroom = list(chatroom)
    # chatroom = chatroom.name
    # print(chatroom)
    cr = [str(r.name) for r in cr]
    temp = {'messages':list(messages),'chatroom':chatroom.name,'chatroomnames': cr}
    return render(request,'chats.html',temp)

def chatsdelete(request,chat_room):
    chatroom = ChatRoom.objects.filter(name=chat_room)[0]
    # We want the user to be removed from the chatroom
    chatroom.user.remove(request.user)
    # chatroom.delete()
    return redirect('/')
