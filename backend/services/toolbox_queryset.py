from django.db.models.query import QuerySet
from rest_framework.request import Request
from django.db.models import  Sum, F
from backend.models import Order, ProductInfo
from django.db.models import Prefetch


def get_queryset_basket_user(request: Request) -> QuerySet:
    basket = Order.objects.filter(
        user_id=request.user.id, state='basket').prefetch_related(
        'ordered_items__product_info__product__category',
        'ordered_items__product_info__product_parameters__parameter').annotate(
        total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
    return basket


def get_queryset_orders_shop(request: Request) -> QuerySet:
    order = Order.objects.prefetch_related(Prefetch('ordered_items__product_info', queryset=ProductInfo.objects.filter(
        shop__user_id=request.user.id))).exclude(state='basket').prefetch_related(
        'ordered_items__product_info__product__category',
        'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
        total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

    return order


def get_queryset_orders_for_send_email(user_id: int, order_id: int) -> QuerySet:
    order = Order.objects.prefetch_related(Prefetch('ordered_items__product_info', queryset=ProductInfo.objects.filter(
        shop__user_id=user_id))).filter(id=order_id).prefetch_related(
        'ordered_items__product_info__product__category',
        'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
        total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

    return order


def get_queryset_orders_user(request: Request) -> QuerySet:
    order = Order.objects.filter(
        user_id=request.user.id).exclude(state='basket').prefetch_related(
        'ordered_items__product_info__product__category',
        'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
        total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
    return order


def get_queryset_order_user(id_order: int) -> QuerySet:
    order = Order.objects.filter(id=id_order).prefetch_related(
        'ordered_items__product_info__product__category',
        'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
        total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
    return order
