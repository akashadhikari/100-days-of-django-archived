from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(User):
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    address = models.CharField(max_length=255)

    def __str__(self):
        full_name = self.first_name + self.last_name
        return full_name
