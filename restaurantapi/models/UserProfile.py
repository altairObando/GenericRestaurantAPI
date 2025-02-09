from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .Contact import Contact, Owner
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='profile')
    owner = models.ForeignKey(Owner, models.CASCADE, null=True, blank=True, related_name='users')
    contact= models.ForeignKey(Contact, models.CASCADE, null=True, blank=True, related_name='profiles')

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    instance.profiles.save()   