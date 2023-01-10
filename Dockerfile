FROM docker.io/python:3.11-slim-bullseye

RUN pip install requests

COPY main.py .
CMD ["python", "./main.py"]
