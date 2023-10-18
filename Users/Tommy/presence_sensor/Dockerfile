FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD presence_sensor.py presence_sensor.py

