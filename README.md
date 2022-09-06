
# API Сервис заказа товаров для розничных сетей.

## Описание

Приложение предназначено для автоматизации закупок в розничной сети. Пользователи сервиса — покупатель (менеджер торговой сети, который закупает товары для продажи в магазине) и поставщик товаров.

**Клиент (покупатель):**

- Пользователь может авторизироваться, регистрироваться и восстанавливать пароль через API.
- Поиск товара. Доступна фильтрация: id(товара), магазин, категория(товар), имя(товар).
- CRUD-операции в корзине, есть возможность дабовлять товары от разных поставщиков.
- Может оформить заказ, отслеживать статус. 

    
**Поставщик:**

- Через API дабовлять/обновлять прайс.
- Может включать и отключать прием заказов.
- Может получать список оформленных заказов (с товарами из его прайса).

**Дополнительные функции:**
- CRUD-операции с контактами пользователей.
- Отправка заказа на email клиента (подтверждение приема заказа).
- Отправка оповещения на email клиента (изменение статуса заказа).
- Отправка заказа на email поставщика (новый заказ).



### Примеры api запросов 
<details>
  <summary>📚 Нажмите, чтобы увидеть некоторые примеры</summary>

[Postman file](./data/api.postman_collection.json)

[Документация Open API](https://app.swaggerhub.com/apis/FROSTILIA/api-service_documentation/1.0.0#/api/api_v1_auth_users_reset_email_create)

</details>
