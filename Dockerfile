FROM python:slim

WORKDIR /foodgram

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000