FROM python:alpine

RUN pip install tornado
ADD . /blockchain

ENTRYPOINT cd /blockchain && python main.py
