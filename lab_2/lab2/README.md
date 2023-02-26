Welcome to the Lab2 Fast Api application..

In order to run the application, we can do this in 3 different modes, and is explained below 

1.) Clone the repo to desired local file and in terminal move to the directory where run.sh is store and run it with the following commands
    
-chmod +x run.sh , this will do the following

-check if the model_pipiline.pkl file exits, else run the trainer.py and create the file and move to the designated folder
 
- run the dockerfile and create the container 
        
- running the docker image to spool up 
        
- testing all the endpoints as expected
        
- stop the docker container
        
- clean up all the container 

2.) Clone the repo to the local file to run the test move to the lab_2/lab2 and run the following command to run the application 
    
-run 'poetry install' to install all the dependancies 
    
-move to lab_2/lab2/src and run the following commands to check if application is running
        
- uvicorn main:app --host 0.0.0.0 --port 8000 or move to ./lab_2 and run the dockerfile to build the docker container and follow below
        
- this should spool up the http server in the localhost
        
- to run the endpoints use the following commands 
        
- -Testing '/hello' endpoint with no name parameter
        
- curl  -X GET "http://localhost:8000/hello"
        
- Testing '/' endpoint.
        
- curl  -X GET "http://localhost:8000/"
        
- -Testing '/docs' endpoint.
        
- curl -X GET "http://localhost:8000/docs"
        
- -Testing '/openapi.json' endpoint
        
- curl -X GET "http://localhost:8000/openapi.json"
        
- -Testing '/predict' endpoint
        
- curl  -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'
        
-Testing '/health' endpoint.
        
-curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"


NOTE:

-'/predict' endpoint is designed to accept multiple inputs, to run the curl -X post command please use the following format

-curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'

-PSA-if the docker container image keeps giving error 'invalid input' please ensure the sklearn is set to scikit-learn = "1.0.2" (this is reflected in poetry.toml)

Question & Answer:

1.)What does Pydantic handle for us? 

-Pydantic is a Python library that handles data validation and settings management. It provides runtime checking and validation of data types, data conversion, and automatic documentation generation for data models. It also supports default values for fields, handles nested data structures, and improves the overall data validation process.

2.)What do GitHub Actions do?

-GitHub Actions is a powerful continuous integration and continuous deployment (CI/CD) tool provided by GitHub. It allows developers to automate their workflows and software development processes with customizable workflows that run in response to events like code commits, pull requests, issues, and more.
By using GitHub Actions, developers can automate many repetitive tasks and reduce the chance of errors, saving time and increasing productivity. It also makes it easier to collaborate on projects, as contributors can easily see the state of the code and the tests that have been run. Additionally, GitHub Actions provides a marketplace of pre-built workflows that developers can easily plug into their own projects to automate common tasks, such as deploying to cloud providers or running tests.

3.)In 2-3 sentences (plain language), describe what the Sequence Diagram below shows.

-This is a sequence diagram showing the flow of data in a basic machine learning application, including the user (U), API (A), and model (M).
The flow starts with the user sending a POST request with a JSON payload to the API. If the input payload does not satisfy the pydantic schema, an error is returned to the user. If the input is valid, the API sends the input values to the model.
The model processes the input values and returns the output values to the API, which stores the returned values. Finally, the API returns the values as an output data model to the user.
Overall, this diagram shows a simple data flow in a machine learning application, where the API acts as an interface between the user and the model.


