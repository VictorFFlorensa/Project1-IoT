FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD processor2.py processor2.py
CMD ["python3", "-u", "processor2.py"]
