FROM python:latest

# Working directory
RUN mkdir -p /app/workdir
WORKDIR /app/workdir

# Copy requirements
COPY requirements.txt /app/workdir/.
COPY run.py /app/workdir/.
COPY app /app/workdir/app

# Install dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install vim -y \
    && pip install --no-cache-dir -r requirements.txt
