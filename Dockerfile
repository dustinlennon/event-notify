FROM python:3.12-alpine3.21

RUN mkdir -p /home/notify

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV PYTHONPATH=/home/notify

COPY app /home/notify/app

ENV NOTIFY_AUX_PATH=/home/notify/aux
VOLUME /home/notify/aux

ENTRYPOINT ["/usr/local/bin/python", "/home/notify/app/notify.py"]
