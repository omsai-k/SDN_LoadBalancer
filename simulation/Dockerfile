FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install Flask requests scikit-learn

ENV PYTHONPATH="/app"

EXPOSE 5000
