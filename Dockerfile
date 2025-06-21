FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "8000", "--log-level", "debug"]
CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "8000", "--log-level", "debug"]




# FROM python:3.11.9-slim

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8000"]


