#!/bin/bash

python todo_manager/manage.py makemigrations
python todo_manager/manage.py migrate
python todo_manager/manage.py createadmin
exec "$@"
