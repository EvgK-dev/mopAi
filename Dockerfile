FROM python:3.13.3-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем системные пакеты
RUN apt-get update && apt-get install -y \
    nano \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости (в том числе gunicorn и gevent)
RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

# Копируем приложение
COPY . /app/

# Устанавливаем переменную среды PATH
ENV PATH="/usr/local/bin:/app:${PATH}"

# Открываем порт (тот же, что в команде запуска)
EXPOSE 8091

# Запускаем Gunicorn с оптимизированными параметрами
CMD ["gunicorn", "mopAi.wsgi:application", \
     "--bind", "0.0.0.0:8091", \
     "--workers", "4", \
     "--worker-class", "gevent", \
     "--timeout", "1800"]
