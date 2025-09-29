# SDN_Architecture

## Overview
A modular, production-ready Software Defined Networking (SDN) simulation platform with ML-based load balancing and threat detection.

## Features
- Modular SDN controllers (core, aggregation, edge) with Flask APIs
- ML modules for load balancing and threat detection
- Secure REST API with authentication and input validation
- Dockerized for production deployment
- Health checks and structured logging
- Environment-based configuration
- Unit and integration tests
- API documentation (Swagger/OpenAPI)
- CI/CD ready (GitHub Actions)

## Quick Start

1. **Clone the repo:**
	```
	git clone <repo-url>
	cd SDN_Architecture
	```
2. **Set up environment:**
	- Copy `.env.example` to `.env` and edit as needed.
	- Install dependencies:
	  ```
	  pip install -r requirements.txt
	  ```
3. **Run with Docker Compose:**
	```
	docker-compose -f simulation/docker-compose.yml up --build
	```
4. **Run tests:**
	```
	pytest tests/
	```

## Production Notes
- Do not commit your virtual environment or secrets.
- Use a real secret key and secure credentials in production.
- See `.env.example` for environment variables.

## API Documentation
- Swagger/OpenAPI docs available at `/docs` endpoint when running.

## License
MIT