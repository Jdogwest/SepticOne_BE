
# FROM python:3.11.9-slim

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "8000", "--log-level", "debug"]



FROM python:3.11.9-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8000"]


