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

COPY --from=build /venv /venv
COPY --from=build /venv/lib/python3.10/site-packages/redis /venv/lib/python3.10/site-packages/redis
ENV PATH /venv/bin:$PATH

COPY . ./

HEALTHCHECK --start-period=15s --interval=15s --timeout=3s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1


ENTRYPOINT ["uvicorn", "lab3.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379



