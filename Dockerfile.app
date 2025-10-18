FROM python:3.13-slim-bullseye

WORKDIR /opt

RUN pip install uv==0.8.19

COPY pyproject.toml /opt/pyproject.toml
COPY uv.lock /opt/uv.lock

RUN uv sync --no-dev

# adding this line to test github actions

# Purposefully copying code last to avoid previous step's cache invalidation
COPY app /opt/app

CMD ["/opt/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
