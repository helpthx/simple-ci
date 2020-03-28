FROM python:3.6
MAINTAINER Joao Vitor R Baptista

ENV PYTHONUNBUFFERED 1

RUN mkdir /Desafio-Coopersystem
WORKDIR /Desafio-Coopersystem
COPY . /Desafio-Coopersystem/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

