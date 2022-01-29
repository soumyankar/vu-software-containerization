# vu-software-containerization
Vrije Universiteit Amsterdam - Software Containerization 2022

To run

```
sudo docker build -t soumyankarm/cats-or-dogs cats-or-dogs/cats-or-dogs-api/api-server/
sudo docker run -p 8888:5000 --name cats-or-dogs soumyankarm/cats-or-dogs
```