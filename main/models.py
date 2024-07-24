from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='main/images/avatars/', blank=True, default='main/images/avatars/default-avatar.png')

    def __str__(self):
        return self.user.username

import main.signals


