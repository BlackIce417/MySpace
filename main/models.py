from django.db import models
from django.contrib.auth.models import User
from topic.models import *

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='main/images/avatars/', blank=True, default='main/images/avatars/default-avatar.png')
    followed_topics = models.ManyToManyField(Room, related_name='followers', through='topic.TopicFollow')
    followed_answers = models.ManyToManyField(AnswersRoom, related_name='followers', through='topic.AnswersFollow')

    def __str__(self):
        return self.user.username

import main.signals


