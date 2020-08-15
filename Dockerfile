FROM ubuntu:18.04

LABEL maintainer="leandro@tecsysbrasil.com.br"
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y python3 
RUN apt-get install -y python3-pip 
RUN mkdir /code
RUN mkdir /log
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/