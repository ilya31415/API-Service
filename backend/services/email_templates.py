from backend.models import ConfirmOrderToken, User
from django.template.loader import render_to_string
from backend.serializers import OrderSerializer
from backend.services.toolbox_queryset import get_queryset_order_user, get_queryset_orders_for_send_email
from backend.tasks import celery_send_email


def send_order_confirmation_email(instance):
    """
    Отправка email клиенту: с ссылкой  для подтверждение заказа
    """
    token, _ = ConfirmOrderToken.objects.get_or_create(order=instance)

    html_template = 'email_confirm_order.html'
    url = {'url': f'http://127.0.0.1:8000/api/v1/confirm/order?key={token.key}',
           'name': instance.user.first_name}
    html_message = render_to_string(html_template, url)

    celery_send_email.delay('Подтверждение заказа!', html_message, instance.user.email)


def send_order_status_update_email(instance):
    """
        Отправка email клиенту: с обновленным статуcом заказа'
    """
    html_template = 'email_update_state_order.html'
    instans = get_queryset_order_user(instance.id)
    serializer = OrderSerializer(instans, many=True)
    html_message = render_to_string(html_template, serializer.data[0])

    celery_send_email.delay('Новый статус заказа!', html_message, instance.user.email)


def send_gratias_ordinis_email(instance):
    """
        Отправка email клиенту: 'Спасибо за заказ'
    """
    html_template = 'email_thanks_order.html'
    instans = get_queryset_order_user(instance.id)
    serializer = OrderSerializer(instans, many=True)

    html_message = render_to_string(html_template, serializer.data[0])
    celery_send_email.delay('Ваш заказ собирается!', html_message, instance.user.email)


def send_shop_new_order_email(instance):
    """
        Отправка email поставщику: уведомление о новом заказе
    """
    html_template = 'email_new_order.html'
    shops_admins = User.objects.filter(shop__product_infos__ordered_items__order=instance.id).distinct()
    for admin in shops_admins:
        data_order = get_queryset_orders_for_send_email(admin.id, instance.id)

        serializer = OrderSerializer(data_order, many=True)

        html_message = render_to_string(html_template, serializer.data[0])
        celery_send_email.delay('Новый заказ!', html_message, admin.email)
