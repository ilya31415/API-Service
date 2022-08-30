from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings as conf_settings
from backend.models import Contact, Order, ConfirmOrderToken, User
from backend.serializers import OrderSerializer

STATE_CHOICES = {'confirmed', 'assembled', 'sent', 'delivered', 'canceled'}


@receiver(post_save, sender=Contact)
def create_contact_order(instance, created, **kwargs):
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
    if instance.state in STATE_CHOICES:

        msg_client = EmailMultiAlternatives(
            # title:
            f"Обновление статуса заказа",
            # message:
            f'Статус Заказа:{instance.state}',
            # from:
            conf_settings.EMAIL_HOST_USER,
            # to:
            [instance.user.email]
        )
        msg_client.send()
        if instance.state =='confirmed':

            shops_admins = User.objects.filter(shop__product_infos__ordered_items__order=instance.id)
            for shop_admin in shops_admins:
                data_message = []

                email = shop_admin.email
                items = instance.ordered_items.filter(product_info__shop__user=shop_admin)

                ser = OrderSerializer(data=items, many=True)
                if ser.is_valid():
                    ser.save()


                    data_message.append(ser.data)
                msg_admin_shop = EmailMultiAlternatives(
                    # title:
                    f"Новый заказ",
                    # message:
                    f'Статус Заказа: {instance.state}\n'
                    f"{data_message}",
                    # from:
                    conf_settings.EMAIL_HOST_USER,
                    # to:
                    [email]
                )
                msg_admin_shop.send()

    elif 'new' == instance.state:
        token, _ = ConfirmOrderToken.objects.get_or_create(order=instance)
        msg = EmailMultiAlternatives(
            # title:
            f"Подтверждение заказа №{instance.id}",
            # message:
            f'http://127.0.0.1:8000/api/v1/confirm/order?key={token.key}',
            # from:
            conf_settings.EMAIL_HOST_USER,
            # to:
            [instance.user.email]
        )
        msg.send()






