# ML Systems

A comprehensive collection of machine learning system implementations focusing on building, deploying, and scaling ML applications using modern technologies and best practices.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Labs](#labs)
  - [Lab 1: FastAPI and Docker Introduction](#lab-1-fastapi-and-docker-introduction)
  - [Lab 2: ML Model Serving with FastAPI](#lab-2-ml-model-serving-with-fastapi)
  - [Lab 3: Kubernetes Deployment with Redis Caching](#lab-3-kubernetes-deployment-with-redis-caching)
  - [Lab 4: Azure Kubernetes Service (AKS) Deployment](#lab-4-azure-kubernetes-service-aks-deployment)
  - [Lab 5: Load Testing and Performance Analysis](#lab-5-load-testing-and-performance-analysis)
- [Final Project](#final-project)
- [Prerequisites](#prerequisites)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Testing](#testing)

## Overview

This repository contains a series of progressive labs that demonstrate the end-to-end workflow for developing and deploying machine learning systems. The labs cover containerization, API development, caching strategies, Kubernetes orchestration, cloud deployment, and performance testing.

## Repository Structure

```
ml_systems/
├── lab_1/                  # FastAPI and Docker basics
│   ├── lab1/               # Source code
│   │   ├── src/            # Application source files
│   │   ├── tests/          # Unit tests
│   │   ├── Dockerfile      # Container configuration
│   │   └── pyproject.toml  # Poetry dependencies
│   └── run.sh              # Automation script
├── lab_2/                  # ML model serving
│   ├── lab2/
│   │   ├── src/            # FastAPI application
│   │   ├── tests/          # Unit tests
│   │   ├── trainer/        # Model training scripts
│   │   └── model_pipeline.pkl
│   └── run.sh
├── lab_3/                  # Kubernetes with Redis caching
│   ├── lab3/
│   │   ├── infra/          # Kubernetes manifests
│   │   └── tests/
│   └── run.sh
├── lab_4/                  # AKS deployment
│   └── lab4/
│       ├── .k8s/           # Kubernetes configurations
│       ├── infra/          # Infrastructure manifests
│       └── build-push.sh   # Container registry script
├── lab_5/                  # Load testing
│   ├── load.js             # K6 load testing script
│   ├── Findings.md         # Performance analysis results
│   └── images/             # Grafana screenshots
└── final_project/          # NLP sentiment analysis API
    ├── finalproject/
    │   ├── finalproject/   # DistilBERT model
    │   ├── infra/          # Kubernetes manifests
    │   ├── tests/          # Unit tests
    │   └── Dockerfile
    └── .k8s/               # AKS deployment configs
```

## Labs

### Lab 1: FastAPI and Docker Introduction

Introduction to building Python APIs with FastAPI and containerizing applications with Docker.

Key concepts:
- FastAPI application setup
- Docker containerization
- Multi-stage Docker builds
- API endpoint testing

```bash
cd lab_1
chmod +x run.sh
./run.sh
```

### Lab 2: ML Model Serving with FastAPI

Serving machine learning models through a REST API using the California Housing dataset.

Key concepts:
- Pydantic data validation
- ML model integration (scikit-learn)
- Poetry dependency management
- GitHub Actions for CI/CD

Endpoints:
- `GET /` - Root endpoint
- `GET /hello` - Hello endpoint with name parameter
- `GET /health` - Health check
- `GET /docs` - OpenAPI documentation
- `POST /predict` - Model prediction endpoint

```bash
cd lab_2
chmod +x run.sh
./run.sh
```

### Lab 3: Kubernetes Deployment with Redis Caching

Deploying the prediction API on a local Kubernetes cluster with Redis caching.

Key concepts:
- Kubernetes deployments and services
- Minikube local cluster
- Redis caching for improved performance
- Namespace isolation

```bash
cd lab_3
chmod +x run.sh
./run.sh
```

### Lab 4: Azure Kubernetes Service (AKS) Deployment

Deploying the application to Azure Kubernetes Service for production-grade hosting.

Key concepts:
- Azure Container Registry (ACR)
- Kustomize overlays (dev/prod)
- Istio virtual services
- kubelogin authentication

```bash
cd lab_4/lab4
chmod +x build-push.sh
./build-push.sh
```

### Lab 5: Load Testing and Performance Analysis

Performance testing the deployed application using K6 and visualizing metrics with Grafana.

Key concepts:
- K6 load testing
- Cache rate impact analysis
- Grafana monitoring
- Performance optimization

Findings summary:
- Cache rate 0.0: 97% success rate, higher latency
- Cache rate 0.5: Improved latency and success rate
- Cache rate 1.0: 100% success rate, significantly reduced latency

See [Findings.md](lab_5/Findings.md) for detailed analysis.

## Final Project

A sentiment analysis API using DistilBERT for NLP-based text classification, deployed on Azure Kubernetes Service.

Features:
- DistilBERT model from HuggingFace for sentiment analysis
- FastAPI REST endpoint
- Redis caching for response optimization
- Kubernetes deployment with autoscaling
- K6 load testing with 0.95 cache rate

Example usage:
```bash
curl -X POST 'https://<your-namespace>.mids255.com/predict' \
  -H 'Content-Type: application/json' \
  -d '{"text": ["I love you!", "I hate you!"]}'
```

See [final_project/README.md](final_project/README.md) for more details.

## Prerequisites

- Python 3.10+
- Docker
- Kubernetes (minikube for local development)
- Poetry (Python dependency management)
- Azure CLI (for AKS deployment)
- K6 (for load testing)

## Technology Stack

| Category | Technologies |
|----------|-------------|
| API Framework | FastAPI |
| ML Libraries | scikit-learn, PyTorch, HuggingFace Transformers |
| Containerization | Docker |
| Orchestration | Kubernetes, Azure Kubernetes Service |
| Caching | Redis |
| Monitoring | Grafana, Prometheus |
| Load Testing | K6 |
| CI/CD | GitHub Actions |
| Dependency Management | Poetry |

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ml_systems
   ```

2. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

3. Navigate to a lab directory and follow the specific README instructions:
   ```bash
   cd lab_2/lab2
   poetry install
   ```

4. Run the application:
   ```bash
   poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

## Testing

Run tests for a specific lab:

```bash
cd lab_2/lab2
poetry run pytest tests/
```

Continuous integration is configured via GitHub Actions. Tests run automatically on push to the main branch.
