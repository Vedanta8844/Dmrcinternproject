from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# from django.contrib.auth import get_user_model
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.
    """
    if created:
        pass


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the user profile when a user is saved.
    """
    instance.profile.save()


# superuser -krish pass-krish
# YourVedBro pass-------
# ShreeRam pass- hanuman@2002 changed to hanuman@forever
