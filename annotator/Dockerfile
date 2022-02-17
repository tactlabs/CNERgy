FROM python:3-alpine3.13

ADD . ./code

WORKDIR /code

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

COPY . /code
RUN pip install -r requirements.txt

EXPOSE 5555

CMD ["python","server.py"]