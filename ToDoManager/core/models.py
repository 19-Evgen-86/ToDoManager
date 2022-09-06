from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    password_repeat = models.CharField(max_length=150,default='')