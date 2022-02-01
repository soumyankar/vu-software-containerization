# VU Software Containerization 2022

### Docker

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