# Base image
FROM python:3.8.10-slim-buster

RUN apt-get update

RUN mkdir /app
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "app/app.py" ]

