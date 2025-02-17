FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U autopep8
RUN pip install -U pycodestyle

ENV PYTHONPATH="/app"