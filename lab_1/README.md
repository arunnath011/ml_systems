Documentation


To run the application, follow these steps:

Open a terminal in the lab_1/ directory.

Run the following command to start the Docker container:
docker run -d -p 8000:8000 --name lab1-container lab1-python:3.10

This will start the lab1-python Docker container in detached mode and 
map port 8000 on the host to port 8000 in the container. The container 
will be named lab1-container.


How to Test the Application
To test the application, follow these steps:

Open a terminal in the lab_1/ directory.

Run the following commands to test the different endpoints of the 
application:

curl_hello=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 
"http://localhost:8000/hello?name=Winegar")
echo "Received status code $curl_hello for '/hello' endpoint"

curl_root=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 
"http://localhost:8000/")
echo "Received status code $curl_root for '/' endpoint"

curl_docs=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 
"http://localhost:8000/docs")
echo "Received status code $curl_docs for '/docs' endpoint"

This will make a GET request to the /hello endpoint with name=Winegar, 
the root / endpoint, and the /docs endpoint, respectively. The HTTP 
status codes returned from the requests will be displayed in the 
terminal.

After testing, don't forget to stop and remove the running Docker 
container:

docker stop lab1-container
docker rm lab1-container


#Answer to the following questions:

1.) What status code should be raised when a query parameter does not 
match our expectations?

Ans- The correct code to raise when a query parameter does not match the 
expectations is a 400 bad request status code. This code indicates that 
the server cannor or will not process the requests due to invalid 
request syntax, unsupported request method, or missing or invalid query 

2.)What does Python Poetry handle for us?

Ans- Python poetry is package dependency management tool for python 
application, it can handle pakcage management, virtual environments, 
package installation and package publishing. overall poetry helps 
stremline the development and distribution of our python applications, 
making it easier to manage packages, dependencies, and virtual 
environments.

3.) What advantages do multi-stage docker builds give us?

Ans- Multistage docker does offer  significant advantages

Reduced Image Size: Multi-stage builds allow us to separate the build 
environment from the runtime environment, meaning that we only include 
the necessary files and dependencies in the final image. This results in 
smaller, more optimized images that are faster to download and deploy.

Improved Security: By using a multi-stage build, we can limit the amount 
of sensitive information that is included in the final image. For 
example, we can build our application with the necessary credentials in 
one stage and then exclude them from the final image.

Improved Reproducibility: Multi-stage builds allow us to create 
reproducible builds by specifying exactly what goes into the final image 
and reducing the possibility of inconsistencies or errors.

Improved Build Performance: By using multi-stage builds, we can cache 
the intermediate stages of our build, reducing build time and improving 
performance.

Better Separation of Concerns: Multi-stage builds allow us to separate 
the build and runtime environments, making it easier to manage and 
maintain our application.

