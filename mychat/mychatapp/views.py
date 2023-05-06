from django.shortcuts import render,redirect
from .models import Friend,Profile,ChatMessage
from .forms import ChatMessageForm
from django.http import JsonResponse
import json
# Create your views here.

def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {
        "user":user,
        "friends":friends,
    }
    return render(request, "index.html",context)

def detail(request,pk):
    friend = Friend.objects.get(profile_id=pk)
    chats = ChatMessage.objects.all()
    user = request.user.profile # msg_sender
    profile = Profile.objects.get(id=friend.profile.id) # msg_reciever
    recieved_chats = ChatMessage.objects.filter(msg_sender=profile,msg_reciever=user)
    recieved_chats.update(seen=True)

    form = ChatMessageForm()

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_msg = form.save(commit=False)
            chat_msg.msg_sender = user
            chat_msg.msg_reciever = profile
            chat_msg.save()
            return redirect("detail",pk=friend.profile.id)


    context = {
        "friend":friend,
        "form":form,
        "profile":profile,
        "user":user,
        "chats":chats,
        "recieved_chats":recieved_chats,
    }
    return render(request, "detail.html",context)


def sendMessage(request,pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    msg = json.loads(request.body)['msg']
    chat_msg = ChatMessage.objects.create(body=msg,msg_reciever=profile,msg_sender=user)
    print(msg)
    return JsonResponse(chat_msg.body,safe=False)

def receivedMessages(request,pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.filter(msg_sender=profile,msg_reciever=user)
    chats_msgs = [chat.body for chat in chats]
    return JsonResponse(chats_msgs,safe=False)

def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    chats_counts=[
        ChatMessage.objects.filter(msg_sender__id=friend.profile.id,msg_reciever=user,seen=False).count() for friend in friends
    ]
    return JsonResponse(chats_counts,safe=False)