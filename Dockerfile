FROM python:alpine

ENV PYTHONUNBUFFERED=1
RUN pip install flask requests pycrypto

ADD . /blockchain

ENTRYPOINT cd /blockchain && python main.py
