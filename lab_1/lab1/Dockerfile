#Dockerfile to build a python3.10 container image for the lab 1 with multi stage (build and run)
#Build stage use slim as base image
FROM python:3.10-slim AS build

#Apt update
RUN set -eux; \ 
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y curl;\
    rm -rf /var/lib/apt/lists/*

#Install Poetry 
ENV POETRY_VERSION=1.3.2
RUN curl -sSL https://install.python-poetry.org | python3 -

# update paths
ENV PATH /root/.local/bin:$PATH


#Copy the pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock ./

#Install the dependencies
RUN python3 -m venv ./venv
RUN . ./venv/bin/activate && poetry install --only main

#Runner
FROM python:3.10-slim AS runner

#Copy the venv from build stage
COPY --from=build /venv /venv

#Set path to venv
ENV PATH /venv/bin:$PATH

#Copy the src/main.py to the container
COPY src/main.py .

#CMD to run uvicorn with log 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
