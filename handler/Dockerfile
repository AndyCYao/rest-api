FROM mysql:5.7

#Create Database
ENV MYSQL_DATABASE lala

# Create tables
COPY mydb.sql /docker-entrypoint-initdb.d/
