#!/bin/bash

# Set the necessary variables
IMAGE_PREFIX=arunnath011
IMAGE_NAME=lab4
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"

# Generate a unique tag for the Docker image based on the current timestamp
TAG=$(date +%Y%m%d-%H%M%S)

# Login to Azure Container Registry
az acr login --name w255mids

# Build the Docker image for the specified platform
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .

# Tag the Docker image with the generated tag and ACR FQDN
docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_FQDN}:${TAG}

# Push the Docker image with the generated tag to ACR
docker push ${IMAGE_FQDN}:${TAG}

# Replace the [TAG] placeholder in the Kubernetes deployment patch file with the generated tag
sed -i.bak "s/\[TAG\]/${TAG}/g" .k8s/overlays/prod/patch-deployment-lab4_copy.yaml

