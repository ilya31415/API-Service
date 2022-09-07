from rest_framework.test import APIClient
import pytest
from model_bakery import baker

from backend.models import Category, User, Shop, Contact, ProductInfo, Product, OrderItem, Order
from rest_framework.authtoken.models import Token

api_url = '/api/v1/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def category_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)

    return factory


@pytest.fixture
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)

    return factory


@pytest.fixture
def contact_factory():
    def factory(*args, **kwargs):
        return baker.make(Contact, *args, **kwargs)

    return factory


@pytest.fixture
def create_token_factory():
    def factory(*args, **kwargs):
        return baker.make(Token, *args, **kwargs)

    return factory


@pytest.fixture
def product_factory():
    def factory(*args, **kwargs):
        return baker.make(Product, _fill_optional=True, *args, **kwargs)

    return factory


@pytest.fixture
def product_info_factory(product_factory):
    def factory(*args, **kwargs):
        return baker.make(ProductInfo, product=product_factory, *args, **kwargs)

    return factory


@pytest.fixture
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, _fill_optional=True, *args, **kwargs)

    return factory


@pytest.fixture
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, _fill_optional=True, *args, **kwargs)

    return factory


@pytest.fixture
def order_factory():
    def factory(*args, **kwargs):
        return baker.make(Order, _fill_optional=True, *args, **kwargs)

    return factory


@pytest.fixture
def order_item_factory():
    def factory(*args, **kwargs):
        return baker.make(OrderItem, _fill_optional=True, quantity=1, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_category(client, category_factory):
    """
    Проверка CategoryView
    """
    category = category_factory(_quantity=5)

    respone = client.get(api_url + 'categories')

    data = respone.json()

    assert respone.status_code == 200
    assert len(data) == len(category)

    for number, item in enumerate(data):
        item_id = item['id']
        for i in category:
            if i.id == item_id:
                assert item['name'] == i.name


@pytest.mark.django_db
def test_get_shop(client, shop_factory):
    """
    Проверка ShopView на получение всех поставщиков
    """
    shop = shop_factory(_quantity=5, state=True)
    shop_factory(_quantity=5, state=False)

    respone = client.get(api_url + 'shops')
    data = respone.json()

    assert respone.status_code == 200
    assert len(data) == len(shop)

    for number, item in enumerate(data):
        assert item['state'] is True
        item_id = item['id']
        for i in shop:
            if i.id == item_id:
                assert item['name'] == i.name


@pytest.mark.django_db
def test_get_my_contact(client, contact_factory, create_token_factory):
    """
    Проверка ContactView на получение своих контактов
    """
    contact = contact_factory()
    token = create_token_factory(user=contact.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    respone = client.get(api_url + 'user/contact/')
    data = respone.json()

    assert respone.status_code == 200
    assert data['city'] == contact.city


@pytest.mark.django_db
def test_access_with_authorization_contact(client, contact_factory):
    """
    Проверка ContactView на отказ в доступе без авторизации
    """

    respone = client.get(api_url + 'user/contact/')

    assert respone.status_code == 401


@pytest.mark.django_db
def test_create_contact(client, create_token_factory):
    """
    Проверка ContactView на создание контактов
    """
    token = create_token_factory()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    contact = Contact.objects.count()

    respone = client.post(api_url + 'user/contact/', data={'city': 'moscow', 'street': 'lubyanka', 'phone': 4456789})
    data = respone.json()

    assert respone.status_code == 201
    assert contact + 1 == Contact.objects.count()
    assert data['city'] == 'moscow'


@pytest.mark.django_db
def test_update_contact(client, contact_factory, create_token_factory):
    """
    Проверка ContactView на обновление контактов
    """
    contact = contact_factory()
    token = create_token_factory(user=contact.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    new_city = 'Moscow'

    respone = client.put(api_url + 'user/contact/', data={'city': new_city})
    data = respone.json()

    assert respone.status_code == 200

    assert data['city'] == new_city


@pytest.mark.django_db
def test_update_contact(client, contact_factory, create_token_factory):
    """
    Проверка ContactView на удаление контактов
    """
    contact = contact_factory()
    token = create_token_factory(user=contact.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    contact_count = Contact.objects.count()

    respone = client.delete(api_url + 'user/contact/', )

    assert respone.status_code == 204
    assert contact_count - 1 == Contact.objects.count()


@pytest.mark.django_db
def test_search_product_info(client, product_info_factory):
    """
    Проверка ProductInfoView на поиск товара
    """
    product_info = product_info_factory(_quantity=5)
    product_shop = product_info[3].shop

    respone = client.get(api_url + f'products/?shop_id={product_shop.id}')
    data = respone.json()

    assert respone.status_code == 200
    assert data[0]['shop'] == product_shop.id


@pytest.mark.django_db
def test_get_partner_state(client, shop_factory, create_token_factory, user_factory):
    """
    Проверка PartnerStateView на получение статусa поставщика
    """
    user = user_factory(type='shop')
    shop = shop_factory(user=user)
    shop_state = shop.state

    token = create_token_factory(user=shop.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    respone = client.get(api_url + 'partner/state')
    data = respone.json()

    assert respone.status_code == 200
    assert data['state'] == shop_state


@pytest.mark.django_db
def test_update_partner_state(client, shop_factory, create_token_factory, user_factory):
    """
    Проверка PartnerStateView на изменение статуса поставщика
    """
    user = user_factory(type='shop')
    shop = shop_factory(user=user)
    past_state = shop.state
    new_shop_state = False

    token = create_token_factory(user=shop.user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    respone = client.put(api_url + 'partner/state', data={'state': new_shop_state})
    data = respone.json()

    assert respone.status_code == 200
    assert past_state != new_shop_state
    assert data['state'] == new_shop_state


@pytest.mark.django_db
def test_get_basket(client, order_item_factory, create_token_factory, user_factory, order_factory, ):
    """
    Проверка BasketView на получение товаров в корзине
    """
    user = user_factory()
    order = order_factory(user=user)

    order_items = order_item_factory(_quantity=5, order=order)

    token = create_token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    respone = client.get(api_url + 'basket/')
    data = respone.json()

    assert respone.status_code == 200
    assert len(data[0]['ordered_items']) == len(order_items)


@pytest.mark.django_db
def test_addendum_product_basket(client, order_item_factory, create_token_factory, user_factory, order_factory,
                                 product_info_factory):
    """
    Проверка BasketView на добавление товара в корзину
    """
    user = user_factory()
    order = order_factory(user=user)
    order_items = order_item_factory(_quantity=5, order=order)

    token = create_token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    new_product = product_info_factory()

    respone = client.post(api_url + 'basket/', data={'product_info': new_product.id, 'quantity': 1})
    data = respone.json()

    assert respone.status_code == 201
    new_order_items = OrderItem.objects.filter(order=order).count()
    assert new_order_items == len(order_items) + 1
