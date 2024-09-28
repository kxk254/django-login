from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Avatar(models.Model):
    avatarid = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.avatarid
    
class User(AbstractUser):
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, default=1)



