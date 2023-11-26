FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD heat_actuator.py heat_actuator.py
CMD ["python3","-u", "heat_actuator.py"]
