FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD temperature_sensor.py temperature_sensor.py
CMD ["python3","-u", "temperature_sensor.py"]
