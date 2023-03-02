# Base image
FROM python:3.8.10-slim-buster

RUN apt-get update

RUN mkdir /app
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV="docker"

EXPOSE 5000

CMD ["python", "src/main.py"]

