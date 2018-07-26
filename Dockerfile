FROM python:alpine

ENV PYTHONUNBUFFERED=1
RUN pip3 install flask requests 

ADD . /blockchain

ENTRYPOINT cd /blockchain && python main.py
