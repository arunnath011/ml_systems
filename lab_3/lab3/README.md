#commnds used 

1.) docker build 
docker build --no-cache -t lab3 .

docker build --no-cache -t lab3 --label pythonapi_lab3 .

2.) docker container 
docker run --name redis -d -p 6379:6379 redis:latest

docker run -p 8000:8000 --link redis:redis lab3

3.) post command to check the endpoint

curl -X POST "http://127.0.0.1:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23},{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'

4.) dont change the scilearn from 1.0.2, incase issue with scikit learn 
update poetry with "poetry self update" and run "poetry update"

5.) command to run the redis in local 
redis-server
to check if its caching 
redis-cli
MONITOR

6.) to run the uvicorn run the command
uvicorn main:app --host 0.0.0.0 --port 8000

Running Docker, first run the redis and then the lab3 


image used for the yaml file for lab3 was downloaded form dockerhub
image: arunnath011/lab3 (i had lot of issues with setting up local registry, found out my firewall was preventing it so used this method
kubernetes:
#commands
minikube start

#Run the following command to set your Docker client to use the Minikube Docker daemon:
eval $(minikube docker-env)
# build your docker image 
docker build -t lab3 .

#create kubernetes cluster, deployment and services 
kubectl create namespace w255lab3
kubectl apply -f infra/ --namespace w255lab3
kubectl get namespaces
kubectl get deployments -n w255lab3
kubectl get services -n w255lab3

#get pods 
kubectl get pods -n w255lab3

# get services
kubectl get svc -n w255lab
# get the logs 
kubectl logs pythonapi-5f7b9dfdf7-t4nbf -n w255lab3

#minikube tunnel
minikube tunnel

#port forward-python api
kubectl port-forward deployment/pythonapi 8000:8000 -n w255lab3

#port forward-redis 
kubectl port-forward -n w255lab3 svc/redis 6379:6379

#to see the caching
MONITOR

# test endpoints
curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23},{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'
