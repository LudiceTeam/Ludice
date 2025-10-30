FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy and install requirements
COPY requirements.txt* ./
RUN if [ ! -f requirements.txt ]; then cp ../requirements.txt .; fi && \
    pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

EXPOSE 8080
CMD ["python", "new.py"]
