FROM python:3-alpine3.13


RUN apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev

WORKDIR /code

COPY . /code
RUN pip install -r requirements.txt

ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1

EXPOSE 8080

CMD ["python","server.py"]


