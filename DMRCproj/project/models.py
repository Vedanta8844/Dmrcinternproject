from PIL import Image
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import get_user_model
# from utils import db
from django.conf import settings

# Create your models here.


class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    file = models.FileField(upload_to='upload/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255, default='')


class FileShare(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='files_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='files_received', on_delete=models.CASCADE)

    file = models.FileField(upload_to='sharedfiles')
    shared_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255, default='')


class Contact(models.Model):

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    desc = models.TextField()

    def __str__(self):
        return self.email


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_users')

    groups = models.ManyToManyField(
        Group, related_name='custom_users')
    profilepic = models.ImageField(
        default='defaultpic.jpg', upload_to='profile_images',)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profilepic.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.profilepic.path)

    def __str__(self):
        return self.username
