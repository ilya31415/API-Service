from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models import Contact, Order


@receiver(post_save, sender=Contact)
def create_contact_order(instance, created, **kwargs):
    if created:
        order = Order.objects.get(user=instance.user, state='basket')
        if order:
            order.contact = instance
            order.save()

