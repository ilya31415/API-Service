from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from backend.services.partner_update import updating_the_price_list_from_file
from backend.models import Category, Shop, Contact, ProductInfo, OrderItem, ConfirmOrderToken
from backend.serializers import CategorySerializer, ShopSerializer, ContactSerializer, ProductInfoSerializer, \
    StateShopSerializer, OrderSerializer, OrderItemSerializer
from backend.permissions import OnlyShops
from backend.services.toolbox_queryset import get_queryset_basket_user, get_queryset_orders_shop, \
    get_queryset_orders_user


class CategoryView(ListAPIView):
    """
    Представление для просмотра категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    """
    Представление для просмотра списка поставщиков
    """
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class ContactView(ModelViewSet):
    """
    Представление для работы с контактами:
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

    def get_queryset(self):
        return ProductInfo.objects.filter(shop__state=True)

    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id', 'shop_id', 'external_id', ]
    http_method_names = ['get']


class PartnerStateView(ModelViewSet):
    """
    Представление, которое реализует работу со статусом поставщика:
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
        basket = get_queryset_basket_user(request)
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)


class PartnerOrders(APIView):
    """
    Класс для получения заказов поставщиками
    """
    permission_classes = [permissions.IsAuthenticated, OnlyShops]

    def get(self, request, *args, **kwargs):
        order = get_queryset_orders_shop(request)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class OrderView(ModelViewSet):
    """
    Класс для получения и размешения заказов пользователями
    """

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_queryset_orders_user(self.request)

    def get_object(self):
        queryset = get_queryset_basket_user(self.request)
        obj = get_object_or_404(queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class ConfirmOrder(APIView):
    """
        Представление для подтверждения  заказа
    """

    def get(self, request, *args, **kwargs):
        key = request.query_params.get('key')

        order_token = ConfirmOrderToken.objects.filter(key=key).first()
        if order_token:
            order_token.order.state = 'confirmed'
            order_token.order.save()
            order_token.delete()

            return Response({"state": True})
        return Response({"state": False})
