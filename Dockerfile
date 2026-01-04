FROM python:latest

# Working directory
RUN mkdir -p /app/workdir
WORKDIR /app/workdir

# Copy requirements
COPY requirements.txt /app/workdir/.

# Install dependencies
RUN apt-get update && apt-get upgrade -y \
    && pip install --no-cache-dir -r requirements.txt
