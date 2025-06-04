from django.db.models.signals import post_save
from django.dispatch import receiver 

from core.models import UserBalance
from .models import CustomUser 


@receiver(post_save, sender=CustomUser)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance)


