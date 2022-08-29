from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from backend.services.partner_update import updating_the_price_list_from_file
from backend.models import Category, Shop, Contact, ProductInfo, Order, OrderItem
from backend.serializers import CategorySerializer, ShopSerializer, ContactSerializer, ProductInfoSerializer, \
    StateShopSerializer, OrderSerializer, OrderItemSerializer
from backend.permissions import OnlyShops
from django.db.models import Q, Sum, F


class CategoryView(ListAPIView):
    """
    Представление для просмотра категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    """
    Представление для просмотра списка магазинов
    """
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class ContactView(ModelViewSet):
    """
    Представление, которое реализует для модели Contact:
    - create,
    - update,
    - delete,
    - retrieve.
    """

    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contact.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PartnerUpdate(APIView):
    """
    Представление для обновления прайса от поставщика
    """

    permission_classes = [permissions.IsAuthenticated, OnlyShops]

    def post(self, request, *args, **kwargs):
        return JsonResponse(updating_the_price_list_from_file(request))


class ProductInfoView(ModelViewSet):
    """
    Пердставление для поиска товаров
    """
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id', 'shop_id', 'external_id', ]
    http_method_names = ['get']


class PartnerStateView(ModelViewSet):
    """
    Представление, которое реализует работу со статусом поставщик:
    - update,
    - retrieve.
    """

    serializer_class = StateShopSerializer
    permission_classes = [permissions.IsAuthenticated, OnlyShops]
    queryset = Shop.objects.all()
    http_method_names = ['get', 'put']

    def get_object(self):
        obj = get_object_or_404(self.queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BasketView(ModelViewSet):
    """
    Представление для работы с корзиной.
    """

    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user, order__state='basket')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user, )

    def get_object(self):
        self.queryset = self.get_queryset()
        obj = get_object_or_404(self.queryset, product_info=self.request.data.get('product_info'))
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)
