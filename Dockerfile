FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
COPY ./app /app
COPY requirements.txt requirements.txt
RUN apt update
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 80