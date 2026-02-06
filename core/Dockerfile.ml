# --- STAGE 1: Builder ---
FROM python:3.9-slim AS builder

WORKDIR /app

# Install ONLY what is needed to compile the libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements_ml.txt .
# Install to a local folder so we can copy it later
RUN pip install --user --no-cache-dir -r requirements/requirements_ml.txt

# --- STAGE 2: Final Production ---
FROM python:3.9-slim

WORKDIR /app

# We still need libpq-dev for the DB driver to run, but NOT the compilers
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-installed libraries from the builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy your code
COPY ./core ./core
COPY ./app/dependencies ./app/dependencies
COPY ml_main.py .

CMD ["uvicorn", "ml_main:app", "--host", "0.0.0.0", "--port", "5000"]