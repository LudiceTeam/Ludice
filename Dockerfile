FROM python:3.9.17-slim

WORKDIR /src

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt