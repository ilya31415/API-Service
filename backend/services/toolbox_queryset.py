from django.db.models.query import QuerySet
from rest_framework.request import Request
from django.db.models import Q, Sum, F
from backend.models import Order


def get_queryset_basket_user(request: Request) -> QuerySet:
    basket = Order.objects.filter(
        user_id=request.user.id, state='basket').prefetch_related(
        'ordered_items__product_info__product__category',
        'ordered_items__product_info__product_parameters__parameter').annotate(
        total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
    return basket


def get_queryset_orders_shop(request: Request) -> QuerySet:
    order = Order.objects.filter(
        ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket').prefetch_related(
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
