from django.db.models.signals import post_save
from django.dispatch import receiver 

from .models import ProfileUser, CustomUser


@receiver(post_save, sender=CustomUser)
def create_profile_for_user(sender, instance, created ,*args, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)
