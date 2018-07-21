FROM ubuntu:latest
MAINTAINER  Andy Yao  <andyyao3@gmail.com>
ADD . /usr/src/tech_challenge

#Build Commands
RUN apt-get update -y
RUN apt-get install -y libmysqlclient-dev python-pip python-dev build-essential


WORKDIR /usr/src/tech_challenge
RUN pip install --no-cache-dir -r requirements.txt


# Run the app
CMD ["python", "app.py"]



