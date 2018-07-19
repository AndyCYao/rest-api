#!/bin/bash

docker run --name lala-run -d -p 8080:8080 lalachallenge
docker run --name db -e MYSQL_ROOT_PASSWORD=test -d -p 3306:3306 mariadb