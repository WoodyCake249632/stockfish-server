FROM python:3.11-slim

WORKDIR /app

# Skopíruj súbory
COPY requirements.txt .
COPY main.py .
COPY stockfish ./stockfish

# Nastav práva na binárku
RUN chmod +x ./stockfish

# Nainštaluj Python závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Spusti aplikáciu
CMD ["python", "main.py"]

