FROM python:3.10-slim as build

RUN apt-get update \
    && apt-get install -y \
        curl\
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*


ENV POETRY_VERSION=1.3.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN python -m venv --copies ./venv
RUN . ./venv/bin/activate && poetry install --only main

FROM python:3.10-slim as run

RUN apt-get update \
    && apt-get install -y \
        curl\
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=build /app .

HEALTHCHECK --start-period=15s --interval=15s --timeout=3s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn" ,"src.main:app","--host","0.0.0.0","--port","8000"]
