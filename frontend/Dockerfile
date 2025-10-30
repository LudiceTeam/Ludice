FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt* ./
RUN if [ ! -f requirements.txt ]; then \
        echo "Using parent requirements.txt"; \
    fi && \
    pip install --no-cache-dir -r requirements.txt 2>/dev/null || \
    pip install --no-cache-dir -r ../requirements.txt

# Copy code
COPY . .

CMD ["python", "app.py"]
