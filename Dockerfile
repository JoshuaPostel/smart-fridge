FROM python:3.6-buster

COPY requirements.txt /root/requirements.txt
COPY src /root/src
COPY data /root/data

RUN pip install -r /root/requirements.txt

WORKDIR /root/src
CMD python -W ignore refrigerator_sim.py
