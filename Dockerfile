
FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "8000", "--log-level", "debug"]




# # Set the working directory inside the container
# WORKDIR /app

# # Copy the requirements file to the working directory
# COPY requirements.txt .

# # Install the Python dependencies
# RUN pip install -r requirements.txt

# # Copy the application code to the working directory
# COPY . .

# # Expose the port on which the application will run
# EXPOSE 8080

# # Run the FastAPI application using uvicorn server
# CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8080"]