FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /Pano360_Project

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt .

# Установка зависимостей
RUN apt update -y && apt upgrade -y
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое директории проекта в контейнер
COPY . .

# Установка переменных окружения
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV DEBUG=1

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Команда для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0"]

