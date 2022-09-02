# !/bin/bash

python ToDoManager/manage.py makemigrations
python ToDoManager/manage.py migrate
python ToDoManager/manage.py createadmin
python ToDoManager/manage.py runserver 0.0.0.0:8000
exec "$@"