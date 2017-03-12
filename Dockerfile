FROM debian:jessie
MAINTAINER Julien Bernard <julien.bernard.iphone@gmail.com>

RUN apt-get update && \
	apt-get install -y build-essential python3 python3-dev python3-pip && \
	pip3 install --upgrade pip && \
	pip3 install pytest flask-restful flask-mongoengine gunicorn passlib pyjwt

RUN mkdir /service

COPY application /service/application

EXPOSE 5000

WORKDIR /service

CMD ["gunicorn","-b",":5000","application.app:app"]