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

`sudo docker build -t flaskapi:v1 services/client/`
`sudo docker tag flaskapi:v1 localhost:32000/flaskapi:v1`
`sudo docker push localhost:32000/flaskapi:v1`

#### Vue
Second, we boot up our front-end image that has been built using Vue.js

`sudo docker build -t frontend:v1 services/server/`
`sudo docker build tag frontend:v1 localhost:32000/frontend:v1`
`sudo docker push localhost:32000/frontend:v1`


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

Add the domain to /etc/hosts to access the UI:
127.0.0.1 mybookslist.com

Test the app with secure hostname(https/tls certificate)

1. [https://mybookslist.com/](https://mybookslist.com/)
1. [https://mybookslist.com/books/ping](https://mybookslist.com/books/ping)
1. [https://mybookslist.com/books](https://mybookslist.com/books)

### Canary Deployment

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

### Contributors

Team Members:  

1. Soumyankar Mohapatra
2. Ander Eguiluz Castañeira
3. Sheejann Tripathi
