FROM python:3-alpine3.13

RUN apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev

ADD ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

WORKDIR /code

COPY . /code

ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1

EXPOSE 8080

CMD ["python","server.py"]


