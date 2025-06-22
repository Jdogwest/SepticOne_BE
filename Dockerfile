# FROM python:3.11.9-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# COPY .env .env

# EXPOSE 8000

# CMD ["fastapi", "app.main:app", "--host", "0.0.0.0", "--proxy-headers", "--port", "8000", "--log-level", "debug"]




# FROM python:3.11.9-slim

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8000"]



# FROM python:3.9

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD { "python ", "main.py" }
