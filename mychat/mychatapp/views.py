from django.shortcuts import render,redirect
from .models import Friend,Profile,ChatMessage
from .forms import ChatMessageForm
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
    }
    return render(request, "detail.html",context)