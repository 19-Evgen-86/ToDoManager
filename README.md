# ToDoManager

Планировщик задач служит для ведения списка дел.
Для удобства использования может быть подключен ТГ-БОТ

# Стек

python3.10, Django, Postgres

# Начало работы

#### ШАГ 1: Установка виртуального окружения:

1. Во вкладке File выберите пункт Settings
2. В открывшемся окне, с левой стороны найдите вкладку с именем
   вашего репозитория (Project: ToDoManager)
3. В выбранной вкладке откройте настройку Python Interpreter
4. В открывшейся настройке кликните на значок ⚙ (шестеренки)
   расположенный сверху справа и выберите опцию Add
5. В открывшемся окне слева выберите Virtualenv Environment,
   а справа выберите New Environment и нажмите ОК

#### ШАГ 2: Установка зависимостей:

Для этого можно воспользоваться графическим интерфейсом PyCharm,
который вам предложит сделать это как только вы откроете файл с заданием.

Или же вы можете сделать это вручную, выполнив следующую команду в терминале:
`pip install -r requirements.txt`

#### ШАГ 3: Создать в корне приложения файл .env со следующими значениями:

- DB_NAME= название БД
- DB_USER= имя пользователя БД
- DB_PASSWORD= пароль для подключения к БД
- DB_HOST= хост размещения БД (по умолчанию localhost)
- DB_PORT= порт на котором работает БД (по умолчанию 5432)
- SECRET_KEY= Секретный ключ
- DEBUG= True (Для продакшен сервера должен быть False)
- VK_OAUTH2_KEY=ID приложения
- VK_OAUTH2_SECRET=защищенный ключ
- TG_TOKEN=токен Телеграмм-бота
-
#### ШАГ 4: Создать приложение в VK и получить токен и секретный ключ

1. Нужно создать приложение в VK https://dev.vk.com
2. Из настроек вашего приложения нужно получить: ID приложения и защищенный ключ.

#### ШАГ 5: Создать бота.

https://core.telegram.org/bots#6-botfather — как создать бота с помощью BotFather.
После создания вы получите сообщение:

- Done! Congratulations on your new bot. You will find it at t.me/metaclassbot. You can now add a description, about
  section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating
  your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational
  before you do this. Use this token to access the HTTP API: <b>2065163148:AAEXg2hysKOwOYggaTY2Ew8uPWnypYlw1r0</b>
  Keep your token secure and store it safely, it can be used by anyone to control your bot.
  For a description of the Bot API, see this page: https://core.telegram.org/bots/api

В сообщении будет токен, который нужно использовать для запросов в Telegram.

#### ШАГ 6: Для локального запуска

1. создаем миграции(manage.py makemigrations)
2. накатить миграции на БД (manage.py migrate)
3. создать суперпользователя для админки (manage.py createsuperuser)
4. запустить проект (manage.py runserver)

# ToDoManager

Планировщик задач служит для ведения списка дел.
Для удобства использования может быть подключен ТГ-БОТ

# Стек

python3.10, Django, Postgres

# Начало работы

#### ШАГ 1: Установка виртуального окружения:

1. Во вкладке File выберите пункт Settings
2. В открывшемся окне, с левой стороны найдите вкладку с именем
   вашего репозитория (Project: ToDoManager)
3. В выбранной вкладке откройте настройку Python Interpreter
4. В открывшейся настройке кликните на значок ⚙ (шестеренки)
   расположенный сверху справа и выберите опцию Add
5. В открывшемся окне слева выберите Virtualenv Environment,
   а справа выберите New Environment и нажмите ОК

#### ШАГ 2: Установка зависимостей:

Для этого можно воспользоваться графическим интерфейсом PyCharm,
который вам предложит сделать это как только вы откроете файл с заданием.

Или же вы можете сделать это вручную, выполнив следующую команду в терминале:
`pip install -r requirements.txt`

#### ШАГ 3: Создать в корне приложения файл .env со следующими значениями:

- DB_NAME= название БД
- DB_USER= имя пользователя БД
- DB_PASSWORD= пароль для подключения к БД
- DB_HOST= хост размещения БД (по умолчанию localhost)
- DB_PORT= порт на котором работает БД (по умолчанию 5432)
- SECRET_KEY= Секретный ключ
- DEBUG= True (Для продакшен сервера должен быть False)
- VK_OAUTH2_KEY=ID приложения
- VK_OAUTH2_SECRET=защищенный ключ
- TG_TOKEN=токен Телеграмм-бота
- ADMIN=имя администратора
- ADMIN_PASSWORD=пароль администратора
#### ШАГ 4: Создать приложение в VK и получить токен и секретный ключ

1. Нужно создать приложение в VK https://dev.vk.com
2. Из настроек вашего приложения нужно получить: ID приложения и защищенный ключ.

#### ШАГ 5: Создать бота.

https://core.telegram.org/bots#6-botfather — как создать бота с помощью BotFather.
После создания вы получите сообщение:

- Done! Congratulations on your new bot. You will find it at t.me/metaclassbot. You can now add a description, about
  section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating
  your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational
  before you do this. Use this token to access the HTTP API: <b>2065163148:AAEXg2hysKOwOYggaTY2Ew8uPWnypYlw1r0</b>
  Keep your token secure and store it safely, it can be used by anyone to control your bot.
  For a description of the Bot API, see this page: https://core.telegram.org/bots/api

В сообщении будет токен, который нужно использовать для запросов в Telegram.

#### ШАГ 6: Для локального запуска

1. создаем миграции(manage.py makemigrations)
2. накатить миграции на БД (manage.py migrate)
3. создать суперпользователя для админки (manage.py createsuperuser)
4. запустить проект (manage.py runserver)

