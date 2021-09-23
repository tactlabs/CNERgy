FROM python:3-alpine3.13



RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

WORKDIR /code

COPY . /code
RUN pip install -r requirements.txt

CMD ["python","server.py"]

