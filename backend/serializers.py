from rest_framework import serializers

from backend.models import Category, Shop, Contact, Product, ProductParameter, ProductInfo, OrderItem, Order

from django.db.utils import IntegrityError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state',)
        read_only_fields = ('id',)


class StateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('state',)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        extra_kwargs = {
            'user': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        return Contact.objects.get_or_create(user=validated_data.pop("user"), defaults=validated_data)[0]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }

    def create(self, validated_data):
        user = validated_data.pop('user')
        order, _ = Order.objects.get_or_create(user=user, state='basket')
        if _:
            try:
                contact = Contact.objects.get(user=user)
                order.contact = contact
                order.save()
            except Contact.DoesNotExist:
                order.contact = None
        try:
            order_items, _ = OrderItem.objects.get_or_create(order=order, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'error': "Для изменения количества товара используйте put запрос"})
        return order_items


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField(default=None)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)

    def validate_state(self, value):
        if 'new' == value:
            if self.instance.contact == None:
                raise serializers.ValidationError({'error': "contact is None"})
        return value
