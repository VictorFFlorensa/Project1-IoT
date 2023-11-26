FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD light_actuator.py light_actuator.py
CMD ["python3","-u", "light_actuator.py"]

