# praktikum_new_diplom foodgram-project-react
##«Фудграм»
Cайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
#  Как работать с репозиторием foodgram_react_project

## Что нужно сделать

Настроить запуск проекта Foodgram в контейнерах и CI/CD с помощью GitHub Actions.
Образы foodgram_frontend, foodgram_backend и foodgram_gateway запушены на DockerHub;
Проект был развернут на сервере: <https://foodgramaline.hopto.org/>
### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker-compose`.
2. Создайте файл `.env`.
3. Выполните команду `docker-compose up -d --buld`.
4. Выполните миграции `sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate`.
5. Создайте суперюзера `sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser`.
6. Соберите статику `sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/`.

# Заполнение базы данных из CSV:
Скрипт загрузки данных в бд находится в recipes > management > commands
Сами csv файлы в backend > foodgram_project > data > csv_import_script.py
Запуск скрипта на запуск импорта всех csv:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py csv_import_script
```

# Примеры запросов к API:
1) Список пользователей:
* Отправить GET-запрос https://foodgramaline.hopto.org/api/users/.
* Ответ придёт в форме:

```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```

2) Регистрация пользователя:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/users/. В теле запроса указать:
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
* Ответ придёт в форме:

```
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```

3) Профиль пользователя:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/users/{id}/.
* Ответ придёт в форме:

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```
4) Текущий пользователь:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/users/me/.
* Ответ придёт в форме:

```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
```
5) Изменение пароля:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/users/set_password/. В теле запроса указать:
```
{
  "new_password": "string",
  "current_password": "string"
}
```
6) Получить токен авторизации:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/auth/token/login/. В теле запроса указать:
```
{
  "password": "string",
  "email": "string"
}
```
* Ответ придёт в форме:

```
{
  "auth_token": "string"
}
```
Поученный токен всегда необходимо передавать в заголовке (```Authorization: Token TOKENVALUE```) для всех запросов, которые требуют авторизации.
7) Удаление токена:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/auth/token/logout/. В теле запроса указать:
8) Cписок тегов:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/tags/.
* Ответ придёт в форме:

```
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
```
9) Получение тега:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/tags/{id}/.
* Ответ придёт в форме:

```
{
  "id": 0,
  "name": "Завтрак",
  "color": "#E26C2D",
  "slug": "breakfast"
}
```
10) Список рецептов:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/recipes/.
* Ответ придёт в форме:

```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
11) Создание рецепта:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/recipes/. В теле запроса указать:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
* Ответ придёт в форме:

```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
12) Получение рецепта:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/recipes/{id}/.
* Ответ придёт в форме:

```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
13) Обновление рецепта:
* Отправить PATCH-запрос https://foodgramaline.hopto.org/api/recipes/{id}/. В теле запроса указать:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
* Ответ придёт в форме:

```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
14) Удаление рецепта:

* Отправить DELETE-запрос http://foodgramaline.hopto.org/api/recipes/{id}/.
15) Список покупок:
* Отправить GET-запрос http://foodgramaline.hopto.org/api/recipes/download_shopping_cart/.
16) Добавить рецепт в список покупок:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/recipes/{id}/shopping_cart/. В теле запроса указать:
```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```
17) Удалить рецепт из списка покупок:
* Отправить DELETE-запрос https://foodgramaline.hopto.org/api/recipes/{id}/shopping_cart/. 
18) Добавить рецепт в избранное:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/recipes/{id}/favorite/. В теле запроса указать:
* Ответ придёт в форме:

{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
19) Удалить рецепт из избранного:
* Отправить DELETE-запрос https://foodgramaline.hopto.org/api/recipes/{id}/favorite/. 
20) Мои подписки:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/users/subscriptions/.
* Ответ придёт в форме:

```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
```
21) Подписаться на пользователя:
* Отправить POST-запрос https://foodgramaline.hopto.org/api/users/{id}/subscribe/.
* Ответ придёт в форме:
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```
21) Отписаться от пользователя:
* Отправить DELETE-запрос https://foodgramaline.hopto.org/api/users/{id}/subscribe/.
22) Список ингредиентов:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/ingredients/.
* Ответ придёт в форме:

```
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```
23) Получение ингредиента:

* Отправить GET-запрос http://foodgramaline.hopto.org/api/ingredients/{id}/.
* Ответ придёт в форме:

```
{
  "id": 0,
  "name": "Капуста",
  "measurement_unit": "кг"
}
```
# Используемые технологии и библиотеки:
В данном проекте использовались Nginx, Postman, Python, Django, Postgres, Docker, GitHub, DockerHub, Django Rest, CSV, github/actions
# Разработчики:
* [![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AlineOdr) Алина Одринская