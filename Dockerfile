FROM docker.io/alpine:3.17.1

RUN apk add --no-cache python3 py3-requests

COPY main.py .
CMD ["python", "./main.py"]
