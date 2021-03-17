FROM python:slim

WORKDIR /foodgram

COPY . .

RUN pip install -r requirements.txt && python manage.py collectstatic --noinput

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
