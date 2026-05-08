FROM python:3.10-slim

WORKDIR /app

# system deps for pillow/opencv may be needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy app files
COPY . /app

EXPOSE 5000

CMD ["gunicorn", "server:app", "-w", "1", "-b", "0.0.0.0:5000"]
FROM python:3.11-slim

# Install system deps needed by OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]
