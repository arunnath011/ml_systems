#!/bin/bash

echo "Building the Docker container"
docker build -t lab1-python:3.10 .

echo "Running the Docker container in detached mode"
docker run -d -p 8000:8000 --name lab1-container lab1-python:3.10

echo "Testing '/hello' endpoint with ?name=Winegar"
curl_hello=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 
"http://localhost:8000/hello?name=Winegar")
echo "Received status code $curl_hello for '/hello' endpoint"

echo "Testing '/' endpoint"
curl_root=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 
"http://localhost:8000/")
echo "Received status code $curl_root for '/' endpoint"

echo "Testing '/docs' endpoint"
curl_docs=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 
"http://localhost:8000/docs")
echo "Received status code $curl_docs for '/docs' endpoint"

echo "Stopping and removing the running Docker container"
docker stop lab1-container
docker rm lab1-container

