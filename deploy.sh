#!/bin/bash


echo "Creating the volume..."

kubectl apply -f ./kubernetes/persistent-volume.yml
kubectl apply -f ./kubernetes/persistent-volume-claim.yml


echo "Creating the database credentials..."

kubectl apply -f ./kubernetes/secret.yml


echo "Creating the postgres deployment and service..."

kubectl create -f ./kubernetes/postgres-deployment.yml
kubectl create -f ./kubernetes/postgres-service.yml



echo "Creating the flask deployment and service..."

kubectl create -f ./kubernetes/flask-deployment.yml
kubectl create -f ./kubernetes/flask-service.yml


echo "Adding the ingress..."

microk8s enable ingress
kubectl apply -f ./kubernetes/mybookslist-ingress.yml


echo "Creating the vue deployment and service..."

kubectl create -f ./kubernetes/vue-deployment.yml
kubectl create -f ./kubernetes/vue-service.yml

echo "Creating the tls-secret"

kubectl apply -f ./kubernetes/tls-secret.yml

echo "creating role and cluster role"

kubectl create -f ./kubernetes/read-only-role.yml
kubectl apply -f ./kubernetes/read-only-binding.yml
kubectl create -f ./kubernetes/cluster-role.yml
kubectl apply -f ./kubernetes/cluster-role-binding.yml
