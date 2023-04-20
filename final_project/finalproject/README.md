order of this build 
1.) make the main.py and test it out locally

2.) build the docker files and test the app in docker container

3.) create minikube deployment using infra and test out the app and the caching 

4.) create run.sh to push the image and tage it

5.) create the .k8s for the AKS and deploy them
    modification from lab4 was to increase the cpu and memory from 200mi and 500mi to 800mi and 2000mi respectively.

6.) test the endpoint at the aks 

7.) load test and record the findings.