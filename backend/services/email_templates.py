from django.conf import settings as conf_settings

from backend.models import ConfirmOrderToken, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from backend.serializers import OrderSerializer
from backend.services.toolbox_queryset import get_queryset_order_user, get_queryset_orders_for_send_email


def send_order_confirmation_email(instance):
    token, _ = ConfirmOrderToken.objects.get_or_create(order=instance)

    html_template = 'email_confirm_order.html'

    url = {'url': f'http://127.0.0.1:8000/api/v1/confirm/order?key={token.key}',
           'name': instance.user.first_name}

    html_message = render_to_string(html_template, url)

    message = EmailMessage('Подтверждение заказа!', html_message, conf_settings.EMAIL_HOST_USER, [instance.user.email])
    message.content_subtype = 'html'
    message.send()


def send_order_status_update_email(instance):
    html_template = 'email_update_state_order.html'
    instans = get_queryset_order_user(instance.id)
    serializer = OrderSerializer(instans, many=True)

    html_message = render_to_string(html_template, serializer.data[0])

    message = EmailMessage('Новый статус заказа!', html_message, conf_settings.EMAIL_HOST_USER, [instance.user.email])
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()


def send_gratias_ordinis_email(instance):
    html_template = 'email_thanks_order.html'
    instans = get_queryset_order_user(instance.id)
    serializer = OrderSerializer(instans, many=True)

    html_message = render_to_string(html_template, serializer.data[0])

    message = EmailMessage('Ваш заказ собирается!', html_message, conf_settings.EMAIL_HOST_USER, [instance.user.email])
    message.content_subtype = 'html'
    message.send()


def send_shop_new_order_email(instance):
    html_template = 'email_new_order.html'
    shops_admins = User.objects.filter(shop__product_infos__ordered_items__order=instance.id).distinct()
    for admin in shops_admins:
        data_order = get_queryset_orders_for_send_email(admin.id, instance.id)

        serializer = OrderSerializer(data_order, many=True)

        html_message = render_to_string(html_template, serializer.data[0])

        message = EmailMessage('Новый заказ!', html_message, conf_settings.EMAIL_HOST_USER, [admin.email])
        message.content_subtype = 'html'
        message.send()
