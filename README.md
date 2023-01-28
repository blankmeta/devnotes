# DevNotes RESTful API

### Проект, созданный для хранения заметок для разработчиков. Реализован на REST-архитектуре с использованием Django Rest Framework.

### Имеется возможность регистрации и аутентификации пользователей с использованием jwt и создания отдельных категорий и заметок.

Последние изменения:
- _Теперь можно поделиться с другими пользователями своей заметкой. При изменении её статуса приватности на публичный автоматически генерируется hash url, по которому любой, у кого есть данная ссылка, может прочитать заметку._

P.S. Фронтенд-составляющая в данный момент активно дописывается.
____

## UI прототипа:

![alt text](https://imageup.ru/img94/4170740/snimok-ekrana-2023-01-19-v-193243.jpg)
____


## Запуск:

- В директории ```./infra``` поднимите контейнеры:

```console
docker-compose up -d --build
```
- После успешного запуска контейнеров, соберите статику:

```console
docker-compose exec web python manage.py collectstatic --no-input
```
- Выполните миграции:

```console
docker-compose exec web python manage.py migrate
```
- Создайте суперюзера:

```console
docker-compose exec web python manage.py createsuperuser
```
___
## Шаблон наполнения .env файла по пути ```./infra/.env```

```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=username
POSTGRES_PASSWORD=password
DB_HOST=db
