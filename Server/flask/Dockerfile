FROM python:3.10.11-slim-bullseye

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

WORKDIR /app
ADD . /app

RUN chown -R uwsgi:uwsgi /app
RUN chmod -R 777 /app

RUN apt-get update && apt-get install -y build-essential libpcre3-dev
RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]