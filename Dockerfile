FROM python:3.12-alpine3.21

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /home/notify
COPY app /home/notify/app

ENV PYTHONPATH=/home/notify
ENV NOTIFY_HOME=/home/notify

VOLUME /home/notify/conf
VOLUME /home/notify/templates

WORKDIR /home/notify

ENTRYPOINT ["/usr/local/bin/python", "app/notify.py"]
