#commnds used 

1.) docker build 
docker build --no-cache -t lab3 .

2.) docker container 
docker run -p 8000:8000 --link redis:redis lab3

3.) post command to check the endpoint

curl -X POST "http://127.0.0.1:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d '{"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23},{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}'

4.) dont change the scilearn from 1.0.2

