#!/bin/bash
python manage.py migrate
python load_test_data.py
python manage.py runserver 0.0.0.0:8000