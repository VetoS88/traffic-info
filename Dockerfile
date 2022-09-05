FROM python:3.9.10-buster
WORKDIR /src
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /src
COPY ./api ./api
COPY main.py .
COPY ./local.env .