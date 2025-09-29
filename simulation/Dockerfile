FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install Flask requests scikit-learn

ENV PYTHONPATH="/app"


EXPOSE 5000

# Healthcheck for Flask app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
	CMD curl --fail http://localhost:5000/health || exit 1
