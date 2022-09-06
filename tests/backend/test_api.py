from rest_framework.test import APIClient
import pytest
from model_bakery import baker

from backend.models import Category, User, Parameter, Shop, Contact

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
def test_get_my_contact(client, contact_factory):
    """
    Проверка ContactView на получение своих контактов
    """
    contact = contact_factory(_quantity=1)


    respone = client.get(api_url + 'shops')
    data = respone.json()

    assert respone.status_code == 200
    assert len(data) == len(contact)

    for number, item in enumerate(data):

        item_id = item['id']
        for i in contact:
            if i.id == item_id:
                assert item['city'] == i.city


