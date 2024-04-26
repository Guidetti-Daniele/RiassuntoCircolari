FROM python:3.10.11-slim-bullseye

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

WORKDIR /app
ADD . /app

RUN chgrp -R uwsgi /app && chmod -R g=u /app

RUN apt-get update && apt-get install -y build-essential libpcre3-dev
RUN pip install -r requirements.txt

USER uwsgi

CMD ["uwsgi", "app.ini"]