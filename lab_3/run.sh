#!/bin/bash

# Start minikube
minikube start

# Set Docker daemon to use Minikube
eval $(minikube docker-env)

# Ensure API model is trained & Check if the model pipeline file exists
model_file=./lab3/model_pipeline.pkl

echo "Checking if model file already exists..."
if [ ! -f "$model_file" ]; then
  echo "Model file does not exist, will need to be created."

  # Check if model file exists in trainer directory and delete it
  model_file_check=./lab3/trainer/model_pipeline.pkl
  if [ -f "$model_file_check" ]; then
    echo "Model file found at $model_file_check. Deleting the file..."
    rm $model_file_check
    echo "$model_file_check deleted."
  fi

  # Train the model and move it to designated folder
  echo "Training California Housing Data Model..."
  cd lab3/trainer
  poetry run python train.py
  cd ..

  echo "Moving the model file to designated folder."
  cp trainer/model_pipeline.pkl $model_file
  rm trainer/model_pipeline.pkl
  echo "$model_file is created and moving to the next step."
else
  echo "Model file already exists. Skipping training step."
fi

# Build Docker container
docker build --no-cache -t lab3 ./lab3

sleep 5

# Apply namespace
kubectl apply -f namespace.yaml

# Apply deployments
kubectl apply -f deployment-redis.yaml
kubectl apply -f deployment-pythonapi.yaml
# Apply services
kubectl apply -f service-redis.yaml
kubectl apply -f service-prediction.yaml

# Create minikube tunnel or port-forward local port
# (replace <your-api-service-name> with the actual name of your API service)
minikube tunnel &
TUNNEL_PID=$!

#port forward-python api
kubectl port-forward deployment/pythonapi 8000:8000 -n w255lab3

# Wait for API to be accessible
until $(curl --output /dev/null --silent --head --fail http://localhost:8000/health); do
    printf '.'
    sleep 5
done

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

echo "Testing '/health' endpoint."
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"


# Clean up after yourself
kill $TUNNEL_PID
kubectl delete all --all -n w255lab3
kubectl delete namespace w255lab3
minikube stop
