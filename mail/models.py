from django.db import models
from accounts.models import User
from datetime import datetime

# Create your models here.


class Conversation(models.Model):
    updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    messenger_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messenger_1', null=True, blank=True)
    messenger_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messenger_2', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)


class Communication(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    read_at = models.DateTimeField(null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING)
    sender_hidden = models.BooleanField(default=False)
    recipient_hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '{}-{}-{}'.format(self.conversation, self.sender.username, self.recipient.username)