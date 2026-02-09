FROM python:3.10-slim


WORKDIR /app


# Update and install only needed system packages
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       g++ \
       git \
       curl \
       wget \
       python3-dev \
       libffi-dev \
       libssl-dev \
       libpq-dev \
       libbz2-dev \
       zlib1g-dev \
       liblzma-dev \
       libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

    


COPY requirements.txt .

RUN pip install --default-timeout=3600 --no-cache-dir -r requirements.txt

COPY . .


CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]

