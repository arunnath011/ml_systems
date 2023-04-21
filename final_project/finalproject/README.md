Order of this build 
1.) make the main.py and test it out locally

2.) build the docker files and test the app in docker container

3.) create minikube deployment using infra and test out the app and the caching locally

4.) create run.sh to push the image and tag it

5.) create the .k8s for the AKS and deploy them
    modification from lab4 was to increase the cpu and memory from 200mi and 500mi to 800mi and 2000mi respectively.

6.) test the endpoint at the aks 

curl -X 'POST' 'https://arunnath011.mids255.com/predict' -L  -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "text": [
                "I love you!",
                  "I hate you!",
                  "I am a Kubernetes Cluster!",
                  "I ran to the store",
                  "The students are very good in this class",
                  "Working on Saturday morning is brutal",
                  "How much wood could a wood chuck chuck if a wood chuck could chuck wood?",
                  "A Wood chuck would chuck as much wood as a wood chuck could chuck if a wood chuck could chuck wood",
                  "Food is very tasty",
                  "Welcome to the thunderdome"
          ]
        }'


7.) load test and record the findings.


Key Learnings:
1.) Making sure the distilbert model is locally installed so it is easier to incorporate into the model and proper functioning
2.) My docker build for AKS deployment kept failing due to memory issues, had to clean out the docker images in the system
3.) Using the run.sh to build the image and pushing to the acr repo is highly recommened as it helps with automated patching for any changes made to the main code base
4.) in deployments need to increase the cpu and the memory size to cpu to 800Mi and memory to 2Gi, this is required as the distilbert and pytorch makes the image size considerably bigger and the model requires higher computational resources to predict the endpoint.
