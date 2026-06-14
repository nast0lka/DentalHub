FROM python:3.12

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]