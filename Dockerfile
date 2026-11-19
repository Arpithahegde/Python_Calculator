
# Stage 1: Build the testing environment
FROM python:3.13-slim AS test

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY tests/ ./tests/

CMD ["python", "-m", "pytest", "-v"]


# Stage 2: Build the application runtime
FROM python:3.13-slim AS runtime

WORKDIR /app

RUN pip install --no-cache-dir Flask gunicorn

COPY app.py .

RUN useradd --create-home appuser

USER appuser

RUN useradd --create-home appuser1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
