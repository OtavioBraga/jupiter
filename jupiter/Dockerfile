FROM python:3.5.3-slim
MAINTAINER Otavio Braga <braganantes@gmail.com>

RUN apt-get update && apt-get -y install libpq-dev gcc

ENV PYTHONUNBUFFERED 1
RUN mkdir /app

RUN mkdir -p /app && mkdir -p /app/static-root && mkdir -p /app/media
WORKDIR /app

RUN groupadd -r django && useradd -r -g django django

ADD requirements/base.txt /app/
RUN pip install -r base.txt

ADD . /app/
COPY ./bin/entrypoint.sh /entrypoint.sh
RUN chown -R django /app \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x bin/manage \
    && chown django bin/manage \
    && chown django -R /app/static-root \
    && chown django -R /app/media

ENV PROJECT_ROOT_DIR /app/jupiter

