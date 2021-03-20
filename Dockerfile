FROM python:slim

WORKDIR /foodgram

COPY . .

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && pip install -r requirements.txt

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
