from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    phonenumber = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    dateofbirth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profilepicture = models.ImageField(upload_to='profileimg/', blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phonenumber','gender']
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

 
    
    def __str__(self):
        return self.email
