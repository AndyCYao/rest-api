FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /src


WORKDIR /src

EXPOSE 8080

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD . /src/flask_app
# Run flask app line here
#ENTRY []
