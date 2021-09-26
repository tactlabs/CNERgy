FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get -y install python3.9
RUN apt-get -y install python3-pip
RUN apt install  build-essential

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

EXPOSE 5555

CMD ["python3","server.py"]


