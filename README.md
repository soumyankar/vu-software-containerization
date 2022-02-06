# VU Software Containerization 2022

### Description
This Github repository contains the required and necessary source code files imperative to _configuring the containers_ and to build the microservices that we have chosen for this application. Currently, we have the following images:  

* Vue.js for the Front-end.
* Flask for the Backend API.
* Postgresql for the Database.

This `README.md` file contains all necessary commands required to __deploy__, __scale__ and, __upgrade__ the application.  

> NOTE: All commands are appended with `sudo` because we built the application on a VM. Please feel > free to modify the commands as you need.  

### Deployment

#### Flask
First, we begin with the Backend API that has been built using Flask. Follow, the commands down below to deploy the backend API

```
sudo docker build -t flaskapi:v1 services/client/
sudo docker tag flaskapi:v1 localhost:32000/flaskapi:v1
sudo docker push localhost:32000/flaskapi:v1
```

#### Vue
Second, we boot up our front-end image that has been built using Vue.js

```
sudo docker build -t frontend:v1 services/server/
sudo docker build tag frontend:v1 localhost:32000/frontend:v1
sudo docker push localhost:32000/frontend:v1
```


### Docker

Now that we have finished with our microservices, we can move onto to using `docker-compose`  
Build the images and spin up the containers:

```sh
$ sudo docker-compose up -d --build
```

Run the migrations and seed the database:

```sh
$ sudo docker-compose exec server python manage.py recreate_db
$ sudo docker-compose exec server python manage.py seed_db
```

Test it out at:

1. [http://localhost:8080/](http://localhost:8080/)
1. [http://localhost:5001/books/ping](http://localhost:5001/books/ping)
1. [http://localhost:5001/books](http://localhost:5001/books)

Run Kubernetes deploy.sh script

`sh deploy.sh`

If the script is not working, run the commands int the deploy.sh manually.


### Ingress
we have already generated a certificate with openssl
The yaml file is applied through the script deploy.sh

Add the domain to /etc/hosts to access the UI:
127.0.0.1 mybookslist.com

Test the app with secure hostname(https/tls certificate)

1. [https://mybookslist.com/](https://mybookslist.com/)
1. [https://mybookslist.com/books/ping](https://mybookslist.com/books/ping)
1. [https://mybookslist.com/books](https://mybookslist.com/books)

### Scaling the app
The deployments can either be added using horizontalpod autoscaler or even manually. The commands are as follows:
`Kubectl autoscale deployment <deployment-name> --min=3 --max=10 --cpu-percent=60`
`kubectl scale deployment <deployment-name> --replicas=3`
 
 Our Flask-api and vue-frontend have 3 replicas on initial deployment.

### Upgrade

#### Deployment Rollout

Since every time we change the Deployment's Pod template a deployment rollout is triggered, we are going to change the Docker image of our flask api to simulate this situation.

Apply the `--record` flag to the deployment command so we can later see the rollout history. Then run `rollout status` to see status of the current deployment.

```sh
$ kubectl apply -f flask-deployment.yaml --record
$ kubectl rollout status deployment/flask
```

Now we can change the image of the container to simulate the rollout and check the status again:

```sh
$ kubectl --record deployment.apps/flask set image deployment.v1.apps/flask flask=jazzdd/alpine-flask
$ kubectl rollout status deployment/flask
```

Finally we can check that the new image is being applied to the pods via the pod-hash-label that should be changing from previous pods to the new deployment. To see the rollout history and the changes made in-between use `kubectl rollout history` as:

```sh
$ kubectl get pods --show-label
$ kubectl rollout history deployment.v1.apps/flask
```


#### Canary Deployment

We should have 5 pods running for our first flask-deployment (v1.0.0). See each pod's version with:

```sh
$ kubectl get pods --show-labels
```

Now we can deploy our second version (1 pod) that would be accessed by 1 out of every 6 users with:

```sh
$ kubectl apply -f flask-deployment-v2.yaml
```

Let's check again the pods and see if the newly created pod for v2 is running:

```sh
$ kubectl get pods --show-labels
```

If v2 works fine, we can scale it to cover v1's replicas with:

```sh
$ kubectl scale deploy flask-v2 --replicas=5
```

Finally we delete the first deployment and we are done. Now every user will use v2 of the application.

```sh
$ kubectl delete deployment flask 
```

### Google Cloud Platform

<img width="1439" alt="Screenshot 2022-02-06 at 18 47 59" src="https://user-images.githubusercontent.com/10772786/152694030-bb7beb8a-38a2-4347-b460-286022f63d2d.png">
Here you see a screenshot of the micro-services hosted and deployed on GCP. To do this, we followed the GKE's personal guide for deployment of Kubernetes applications.   
First, we created a `cloudbuild.yaml` file to show the deployment files annd the clusters that were used during the initialization on GCP.  
Second, we created a `deployment.yaml` file. This file is more complicated and tricky to write because we need to show, and define the services. 

Finally, now that we had our config for our application's Services, it is possible to create the services on our cluster.
Steps:
1. Enable Kubernetes API on GCP
2. Create a New Kubernetes cluster
3. Add a node pool for our micro-services.

Now that GCP is ready to host our micro-services, we can fire it up by:
`sudo gcloud builds submit --project=vu-software-containerization --config cloudbuild.yaml`

### Contributors

Team Members:  

1. Soumyankar Mohapatra
2. Ander Eguiluz Castañeira
3. Sheejann Tripathi
