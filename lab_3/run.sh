#!/bin/bash

# Start minikube
echo "starting Minikube..."
minikube start

# Set Docker daemon to use Minikube
echo "Setting Docker deamon to use in Minikube..."
eval $(minikube docker-env)

# Build Docker container
echo "Docker container build..."
docker build --no-cache -t lab3 ./lab3

sleep 5

cd lab3/infra

# Apply namespace
echo "starting Kubernetes..."
kubectl apply -f namespace.yaml

# Apply deployments
kubectl apply -f deployment-redis.yaml
kubectl apply -f deployment-pythonapi.yaml
# Apply services
kubectl apply -f service-redis.yaml
kubectl apply -f service-prediction.yaml

# Create minikube tunnel or port-forward local port
echo "starting Minikube tunnel..."
minikube tunnel &
TUNNEL_PID=$!

#port forward-python api
echo "port forward..."
kubectl port-forward deployment/pythonapi 8000:8000 -n w255lab3

sleep 5


# Wait for API to be accessible
echo "Waiting for API to be accessible..."
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
echo "Shutting down the Minikube Tunnel and deleting the k8s namespace..."
kill $TUNNEL_PID
kubectl delete all --all -n w255lab3
kubectl delete namespace w255lab3
minikube stop


echo "Run done!!, time for coffee?..."