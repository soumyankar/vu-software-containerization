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

Test the app with secure hostname(https/tls certificate)

[https://mybookslist.com/](https://mybookslist.com/)
[https://mybookslist.com/books/ping](https://mybookslist.com/books/ping)
[https://mybookslist.com/books](https://mybookslist.com/books)

### Contributors

Team Members:  

1. Soumyankar Mohapatra
2. Ander Eguiluz Castaneira
3. Sheejann Tripathi
