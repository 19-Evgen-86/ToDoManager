# ToDoManager

Планировщик задач

# Стек

python3.10, Django, Postgres

# Функционал

- Создание/просмотр/редактирование/удаление категорий.
- Создание/просмотр/редактирование/удаление целей.
- Создание/просмотр/редактирование/удаление комментариев.
- вход через социальную сеть VK.
- поддержка телеграмм бота

# Начало работы

##### ШАГ 1: Установка зависимостей:

`pip install -r requirements.txt`

##### ШАГ 2: Создать в корне приложения файл .env со следующими значениями:

- DB_NAME= название БД
- DB_USER= имя пользователя БД
- DB_PASSWORD= пароль для подключения к БД
- DB_HOST= хост размещения БД (по умолчанию localhost)
- DB_PORT= порт на котором работает БД (по умолчанию 5432)
- SECRET_KEY= Секретный ключ
- DEBUG= True (Для продакшен сервера должен быть False)
- TG_TOKEN = токен телеграмма

##### ШАГ 3: Создать БД, сделать миграции

- запустить контейнеры `docker-compose up -d`
- запустить скрипт `sh migrate-start.sh`

## Создание Телеграмм бота

- Создать бота с помощью бота BotFather внутри Telegram.
  https://core.telegram.org/bots#6-botfather — как создать бота с помощью BotFather.