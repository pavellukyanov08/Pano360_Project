FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /Pano360_Project

COPY requirements.txt .

RUN apt update -y && apt upgrade -y
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV DEBUG=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

