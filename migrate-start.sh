#!/bin/bash

python ToDoManager/manage.py makemigrations
python ToDoManager/manage.py migrate
python ToDoManager/manage.py createadmin
python ToDoManager/manage.py collectstatic

exec "$@"
