from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Avatar(models.Model):
    avatarid = models.CharField(max_length=30, primary_key=True)
    avatarurl = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.avatarid

class DarkMode(models.Model):
    mode_value = models.CharField(max_length=30, null=True, blank=True)
    text_value = models.CharField(max_length=30, null=True, blank=True)
    bg_value = models.CharField(max_length=30, null=True, blank=True)
    nav_value = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.mode_value

class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    darkmode = models.ForeignKey(DarkMode, on_delete=models.CASCADE)

    def __str__(self):
        return self.user