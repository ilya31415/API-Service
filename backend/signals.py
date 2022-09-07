from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models import Contact, Order

from backend.services.email_templates import send_order_confirmation_email, send_order_status_update_email, \
    send_gratias_ordinis_email, send_shop_new_order_email

STATE_CHOICES = {'confirmed', 'assembled', 'sent', 'delivered', 'canceled'}


@receiver(post_save, sender=Contact)
def create_contact_order(instance, created, **kwargs):
    """
    Дабовление новых контактов в корзине
    """
    if created:
        try:
            order = Order.objects.get(user=instance.user, state='basket')
        except Order.DoesNotExist:
            order = False
        if order:
            order.contact = instance
            order.save()


@receiver(post_save, sender=Order)
def send_email_after_changing_order_status(instance, created, **kwargs):
    """
    Отправка email при изменение статуса в заказе
    """

    if instance.state in STATE_CHOICES:
        # оповещение о изменение статуса заказа
        send_order_status_update_email(instance)

    if 'confirmed' == instance.state:
        # оповещение покупателя
        send_gratias_ordinis_email(instance)
        # оповещение поставщиков о новом заказе
        send_shop_new_order_email(instance)

    elif 'new' == instance.state:
        # отправка emal для подтверждения заказа
        send_order_confirmation_email(instance)
