FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD topic-partition-creator.py topic-partition-creator.py
CMD ["python3", "-u", "topic-partition-creator.py"]



