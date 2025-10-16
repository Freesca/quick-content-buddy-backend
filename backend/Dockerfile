FROM python:3.11-slim

WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e installa requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il progetto
COPY . .

# Rendi eseguibile manage.py
RUN chmod +x manage.py

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]