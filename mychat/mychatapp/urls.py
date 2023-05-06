from django.urls import path
from .views import index,detail,sendMessage,receivedMessages,chatNotification
urlpatterns = [
    path("",index,name="index"),
    path("friends/<int:pk>",detail,name="detail"),
    path("send_msg/<int:pk>",sendMessage,name="send_msg"),
    path("receive_msgs/<int:pk>",receivedMessages,name="receive_msgs"),
    path("chat_notification",chatNotification,name="chat_notification")
]