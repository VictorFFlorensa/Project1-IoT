FROM python:3.9.14-slim
RUN mkdir script
WORKDIR script
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD clean-processor.py clean-processor.py
CMD ["python3", "-u", "clean-processor.py"]
