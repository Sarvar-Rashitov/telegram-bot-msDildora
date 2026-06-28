#!/bin/bash
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate


# Setup webhook
python manage.py setup_webhook
