#!/bin/bash

#had to note down my prefix as the other method was giving the wrong id
IMAGE_PREFIX=arunnath011

#FQDN = Fully-Qualified Domain Name

IMAGE_NAME=lab4
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"

az acr login --name w255mids

docker build --platform linux/amd64 -t ${IMAGE_NAME} .

docker tag ${IMAGE_NAME} ${IMAGE_FQDN}

docker push ${IMAGE_FQDN}

