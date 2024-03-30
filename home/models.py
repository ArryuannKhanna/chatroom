from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    user = models.ManyToManyField(User,related_name= 'chatrooms')
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name


class Messages(models.Model):
    chatroom = models.ForeignKey(ChatRoom,related_name= 'messages',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name= 'messages',on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

