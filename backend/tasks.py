from django.core.mail import EmailMessage
from django.conf import settings as conf_settings
from celery import shared_task
from django.utils.safestring import SafeString


@shared_task()
def celery_send_email(title: str, html_message: SafeString, email: str):
    """
    Отправка email используя celery
    """
    message = EmailMessage(title, html_message, conf_settings.EMAIL_HOST_USER, [email])
    message.content_subtype = 'html'
    message.send()
