# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  

class User(AbstractUser):

 pass
 
 
class Profile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=200, blank=True) 

    def __str__(self):
        return f"{self.user.username}의 프로필"