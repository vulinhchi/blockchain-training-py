FROM python:alpine

RUN pip install flask
ADD . /blockchain

ENTRYPOINT cd /blockchain && python main.py
