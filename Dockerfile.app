FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt update
RUN pip install --no-cache-dir --upgrade -r requirements.txt
WORKDIR /code/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80