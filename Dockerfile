FROM python:3.13-alpine

WORKDIR /usr/src/core

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .
