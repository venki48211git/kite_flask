# Base image is amazon Linux
FROM amazonlinux:latest

ENV TZ="Asia/Calcutta"

RUN yum install -y git pip

WORKDIR /usr/src/app

RUN python3 -m venv /usr/src/app

RUN . /usr/src/app/bin/activate

COPY g3.py /usr/src/app

COPY g3_web.py /usr/src/app

COPY config.py /usr/src/app

COPY data.csv /usr/src/app

COPY symbol.csv /usr/src/app

COPY templates /usr/src/app/templates

RUN /usr/src/app/bin/pip install -U git+https://gitlab.com/algo2t/kiteext.git

RUN /usr/src/app/bin/pip install --no-cache-dir pyotp requests websocket_client pandas pyyaml flask tabulate

#EXPOSE 5000

CMD ["/usr/src/app/bin/python3", "/usr/src/app/g3_web.py"]
