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
redis-cli

#to see the caching
MONITOR

# test endpoints
curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23},{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'



#Answer the following questions:


What are the benefits of caching?
Caching can also reduce the workload on servers by reducing the number of requests for the same data. This can help to prevent servers from becoming overloaded and crashing during periods of high traffic.
It can Caching can significantly improve performance by reducing the amount of time it takes to fetch or generate data. By storing frequently used data in a cache, subsequent requests for that data can be served more quickly, reducing response times and improving the user experience.
Caching can reduce latency by serving data from a cache located closer to the user, reducing the amount of time it takes for data to travel over a network.
Process of caching can reduce bandwidth usage by serving cached data instead of retrieving the data from a server. This can help to reduce the cost of hosting and improve the efficiency of network traffic.
Ability to scale by allowing resources to be reused more efficiently. By caching frequently used data, resources can be freed up to handle other tasks, allowing the system to handle more requests without requiring additional resources.


What is the difference between Docker and Kubernetes?
Docker is a platform which allows for conternization of application to the developers to a package with all the required dependencies into a single container, that can be consistent across different environments. This method helps it easier to deploy applications and ensures that they can run reliable and consistently. 
On the other hand Kunernetes is a container orchestration tool that assiste in managing containers and services across multiple nodes/machines. Kubernetes helps with automating the deployment, scaling and management of the containerized application and can  used to manage large and complex distributed systems.


What does a kubernetes deployment do?
A Kubernetes deployment is in charge of setting up and maintaining instances of a Kubernetes application. It handles the deployment's rollout strategy and makes sure the desired number of application replicas are up and running.
A Kubernetes deployment enables declarative updates to the application, which means that the user describes the intended state of the application and Kubernetes takes care of the specifics of updating the running instances to meet that desired state. Moreover, it allows rolling updates, allowing for the steady rollout of new application versions across the replicas with the least amount of downtime.
In conclusion, a Kubernetes deployment offers a simple and automatic approach to manage a Kubernetes application's lifetime, from setting up replicas to scaling and upgrading them.

What does a kubernetes service do?
In Kubernetes, a service is an abstraction layer that provides a stable network endpoint for a set of pods. It allows clients to access the pods through a single IP address, load balances traffic between the pods, and provides automatic service discovery for pods within the cluster.
Services in Kubernetes can be of different types, including ClusterIP, NodePort, LoadBalancer, and ExternalName, each with its own set of features and use cases. ClusterIP services provide a stable IP address that is only reachable from within the cluster, while NodePort services allow access to the pods from outside the cluster by opening a port on each node in the cluster. LoadBalancer services provide external load balancing capabilities, and ExternalName services allow services to be mapped to external DNS names.
Overall, Kubernetes services help to provide reliable and scalable communication between pods in a cluster, while abstracting the underlying network details from the end user.
