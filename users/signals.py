from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NewUser, Client, Employee


# Client profile
@receiver(post_save, sender=NewUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "Клиент":
            Client.objects.create(user=instance)
            print("Profile created")


# Employee profile
@receiver(post_save, sender=NewUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role != "Клиент":
            Employee.objects.create(user=instance)
            print("Profile created")

