FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get -y install python3.9
RUN apt-get -y install python3-pip
RUN apt install python3-dev \
                        build-essential  zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
                        libreadline-dev libffi-dev wget \
                        linux-libc-dev

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

RUN chmod 400 ./run.sh

EXPOSE 5555

CMD ["./run.sh"]


