from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .Contact import Contact, Owner

class UserProfile(models.Model):
    ROLES = (
        ('OWNER', 'Owner'),
        ('WAITER', 'Waiter'),
        ('KITCHEN', 'Kitchen Staff'),
        ('CASHIER', 'Cashier'),
    )
    
    user = models.OneToOneField(User, models.CASCADE, related_name='profile')
    owner = models.ForeignKey(Owner, models.CASCADE, null=True, blank=True, related_name='users')
    contact = models.ForeignKey(Contact, models.CASCADE, null=True, blank=True, related_name='profiles')
    role = models.CharField(max_length=20, choices=ROLES, null=True, blank=True)
    active_location = models.ForeignKey('RestaurantLocations', models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role or 'No role'}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.role:
            group_name = self.role.lower()
            group, _ = Group.objects.get_or_create(name=group_name)
            self.user.groups.add(group)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    instance.profile.save()