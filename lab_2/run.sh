#!/bin/bash

# Check if the model pipeline file exists
model_file=./lab2/model_pipeline.pkl

echo "Checking if model file already exists..."
if [ ! -f "$model_file" ]; then
  echo "Model file does not exist, will need to be created."

  # Check if model file exists in trainer directory and delete it
  model_file_check=./lab2/trainer/model_pipeline.pkl
  if [ -f "$model_file_check" ]; then
    echo "Model file found at $model_file_check. Deleting the file..."
    rm $model_file_check
    echo "$model_file_check deleted."
  fi

  # Train the model and move it to designated folder
  echo "Training California Housing Data Model..."
  cd lab2/trainer
  poetry run python train.py
  cd ..

  echo "Moving the model file to designated folder."
  cp trainer/model_pipeline.pkl $model_file
  rm trainer/model_pipeline.pkl
  echo "$model_file is created and moving to the next step."
else
  echo "Model file already exists. Skipping training step."
fi

# Build and run the Docker container
echo "Building lab2 Docker image."
docker build --no-cache -t lab2 ./lab2

echo "Running the lab2 container."
docker run -d --name lab2app -p 8000:8000 lab2

sleep 5

# Test endpoints
echo "Testing endpoints..."

echo "Testing '/hello' endpoint with '?name=Winegar'."
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Winegar"

echo "Testing '/hello' endpoint with no name parameter."
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello"

echo "Testing '/' endpoint."
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "Testing '/docs' endpoint."
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "Testing '/openapi.json' endpoint."
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

echo "Testing '/predict' endpoint."
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'

# Stop and remove the Docker container
docker stop lab2app
docker rm lab2app

# Clean up Docker resources
echo "Cleaning up Docker images..."
docker system prune -af
