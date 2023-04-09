Commands used for this part

step-1:
installing the k6 

step-2 
modifying the load.js file to accomodate your data schema and health schema
changes made for this work 
1.) /predict endpoint, i use scheme which looks like this {
  "data": [
    {
      "MedInc": 8.3252,
      "HouseAge": 41.0,
      "AveRooms": 6.98412698,
      "AveBedrms": 1.02380952,
      "Population": 322,
      "AveOccup": 2.55555556,
      "Latitude": 37.88,
      "Longitude": -122.23
    }
  ]
}

hence modified the load.js code  as below 
return {
        data: [input]
    }


2.) /health endpoint:
added the status check =='ok', as this is what was on my lab4.main file
check(healthRes, {
        'is 200': (r) => r.status === 200,
        'status healthy': (r) => r.json('status') === 'ok',
    })

Step-3

start the grafana by using this command below 
kubectl port-forward -n prometheus svc/grafana 3000:3000

Step-4

in lab_5 dir, run the command 'k6 run load.js' (need to install k6 before doing this step)