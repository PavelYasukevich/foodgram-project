[![Foodgram workflow](https://github.com/PavelYasukevich/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)](https://github.com/PavelYasukevich/foodgram-project/actions/workflows/foodgram_workflow.yaml)

# Disclaimer

Это **учебный** проект, сделанный в рамках курса Python backend developer. Весь **frontend** для проекта был предоставлен в рамках курса, и не является написанным мною.

# Проект Foodgram - продуктовый помощник

Foodgram - это продуктовый помощник, сервис для публикации рецептов с возможностью составить список покупок для приготовления выбранных блюд.

## Использованные технологии

* [Django](https://www.djangoproject.com/) - Веб-фреймворк, версия 3.0.8
* [DRF](https://www.django-rest-framework.org/) - Django REST API фреймворк, версия 3.11.0
* [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP сервер для UNIX, версия 20.0.4
* [PostgreSQL](https://www.postgresql.org/) - База данных, версия 13.2
* [Docker](https://docs.docker.com/) - Контейнеризация, версия 20.10.3
* [Docker-compose](https://docs.docker.com/compose/) версия 1.28.3

## Локальный запуск
1. Клонируйте репозиторий.
2. Выберите ветку local_deploy `git checkout local_deploy`
3. Установите зависимости `pip install -r requirements.txt`
4. Для фунционала скачивания списка ингредиентов понадобится [wkhtmltopdf](https://wkhtmltopdf.org/)
5. В базе загружен список ингредиентов, тэги фильтрации. Логин\пароль суперпользователя **admin\admin**

## Авторы

* **Pavel Yasukevich** - [GitHub profile](https://github.com/PavelYasukevich)

## Лицензия

Проект использует лицензию MIT - [LICENSE.md](LICENSE.md)
