FROM python:3.12-alpine3.21

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV PYTHONPATH=/home/app
WORKDIR /home/app

CMD ["/usr/local/bin/twistd", "-ny", "/home/app/server.tac"]
