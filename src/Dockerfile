# Lekki obraz z Pythonem
FROM python:3.11-slim

# Lepsze logi i brak zbędnych plików .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Katalog roboczy w kontenerze
WORKDIR /app

# Najpierw kopiujemy requirements (Docker cache)
COPY requirements.txt .

# Instalacja bibliotek
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały kod aplikacji
COPY . .

# Port Streamlit
EXPOSE 8501

# Start aplikacji
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]