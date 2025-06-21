# FROM python:3.11.9-slim

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--proxy-headers", "--port", "8000"]

# Базовый образ Python
FROM python:3.11.9-slim

# Установка зависимостей для сборки и работы с PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Порт, который будет использовать uvicorn
EXPOSE 8000

# Команда запуска — пока просто bash, чтобы не упал
CMD ["bash"]
