<div id="header" align="left">
    <img src="https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow" alt="Python"/>
    <img src="https://img.shields.io/badge/Django-dark_green?logo=django&logoColor=white" alt="Django"/>
    <img src="https://img.shields.io/badge/Django-rest-red?logo=django&logoColor=white" alt="Django Rest"/>
</div>

# Проект YaMDb

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

## Технологии используемые в проекте:
- python==3.9.13
- requests==2.26.0
- Django==3.2
- djangorestframework==3.12.4
- PyJWT==2.1.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- django-import-export==3.2.0
- blue==0.9.1
- isort==5.12.0
- djangorestframework_simplejwt==5.2.2
- django-filter==23.2


## Инструкция по запуску

1) Клонировать репозиторий и перейти в него в командной строке:

```
git clone --single-branch --branch master https://github.com/xSergey10/api_yamdb.git
```

```
cd api_yamdb
```

2) Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3) Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
4) Прозвести настройки проекта
```
Переименовать .env.example в .env и заполнить SECRET_KEY своим ключем
```
5) Выполнить миграции:

```
python manage.py migrate
```
6) Создать суперпользователя:

```
python manage.py createsuperuser
```
7) Запустить проект:

```
python manage.py runserver
```


## Как наполнить БД
Порядок и схема добавления CSV в БД.
Находясь на ресурсе http://127.0.0.1:8000/admin/ проделать пошагово файлы.
Все файлы для импорта лежат в папке проекта static/data
```
1) Пользователи --> users.csv
```
```
2) Жанры --> genre.csv
```
```
3) Категории --> category.csv
```
```
4) Произведения и жанры --> genre_title.csv
```
```
5) Произведения --> titles.csv
```
```
6) Отзывы --> review.csv
```
```
7) Комментарии --> comments.csv
```

## Авторы
#### Первоначальное авторское право © 2020 Яндекс.Практикум <https://github.com/yandex-praktikum>
#### Раздвоенное авторское право © 2023 Сергей Серов
#### Раздвоенное авторское право © 2023 Александр Тарасов
#### Раздвоенное авторское право © 2023 Андрей Скляров