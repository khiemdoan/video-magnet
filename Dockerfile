FROM python:3.11-slim AS base

LABEL author=doankhiem.crazy@gmail.com

ENV PYTHONUNBUFFERED=1

FROM base AS builder

ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ADD https://install.python-poetry.org/ /tmp/install-poetry.py
RUN python /tmp/install-poetry.py && rm /tmp/install-poetry.py

WORKDIR /build

COPY pyproject.toml poetry.lock .
RUN python -m venv /venv \
    && . /venv/bin/activate \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main --no-interaction --no-ansi

FROM base AS final

RUN groupadd appgroup && useradd -g appgroup -m appuser

USER appuser

COPY --from=builder /venv/ /venv/

WORKDIR /app

COPY . .

ENV PATH=/venv/bin:$PATH

CMD ["python", "main.py"]
