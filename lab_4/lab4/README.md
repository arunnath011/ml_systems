#Notes for Lab_4

#Steps for aks deployment 
1.) install kubelogin
2.)docker build the image  & push it using the build-push.sh command(in my case used the docker build for M1 chip, commands in following section) 
3.)convert the kubelogin from minikube to azure
4.) login into aks 
5.) apply the virtual services
6.) apply deployment
7.) check the deployments
8.) check the services
8.) check the endpoints with the respective commands

# install Also needed to install the kuectl login tool and enable it using the following commands
brew install Azure/kubelogin/kubelogin

#docker build the image and pushing the image to acr 
sh build-push.sh

#adding azure-cli
kubelogin convert-kubeconfig -l azurecli

# commands used 
Change your kubernetes context between the AKS cluster and minikube
kubectl config use-context w255-aks

# login:
az acr login --name w255mids

#adding virtual services
kubectl apply -f virtual-service.yaml

# deployment:
run the below commands from base, overlay/prod, overlay/dev

kubectl apply -k .

# to check deployments:
kubectl get deployments -n arunnath011

# to check services:
kubectl get services  -n arunnath011

# running the various endpoints, the commands will return 200 for OK and 402 if its not running ok


#NOTE: /hello endpoint doesnt seem to be working well, i have heard from the discussion board its ok if its not working ok


 Testing '/hello' endpoint with '?name=Winegar'.
curl -o /dev/null -s -w "%{http_code}\n" -X GET "https://arunnath011.mids255.com/hello?name=Winegar"

# Testing '/hello' endpoint with no name parameter.
curl -o /dev/null -s -w "%{http_code}\n" -X GET "https://arunnath011.mids255.com/hello"

# Testing '/' endpoint.
curl -o /dev/null -s -w "%{http_code}\n" -X GET "https://arunnath011.mids255.com/"

# Testing '/docs' endpoint.
curl -o /dev/null -s -w "%{http_code}\n" -X GET "https://arunnath011.mids255.com/docs"

# Testing '/openapi.json' endpoint.
curl -o /dev/null -s -w "%{http_code}\n" -X GET "https://arunnath011.mids255.com/openapi.json"

# Testing '/predict' endpoint.
curl -o /dev/null -s -w "%{http_code}\n" -X POST 'https://arunnath011.mids255.com/predict' -L -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'

#Command used for /predict if you want to see the output results

curl -X 'POST' 'https://arunnath011.mids255.com/predict' -L -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'


