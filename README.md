# GridBridge Smart Meter QA

GridBridge Smart Meter QA is an independent learning and portfolio project demonstrating API development and automated testing for smart-meter systems using FastAPI, MySQL, PyTest, JWT authentication and Allure reporting.

The project models common smart-meter concepts including meter management, OBIS-based measurement data, meter events, user tasks, communication configuration and API security.

## Quick Start

1. Copy `.env.example` to `.env` and configure the local environment. Never commit `.env`.
2. Initialize MySQL using `scripts/schema.sql`.
3. Install dependencies with `uv sync --dev` or `pip install -r requirements.txt`.
4. Start the API:
   `uv run uvicorn app.main:app --reload --port 8001`
5. Open Swagger:
   `http://127.0.0.1:8001/docs`
6. Run automated tests:
   `uv run pytest -v`
7. Generate Allure results:
   `uv run pytest --alluredir=allure-results`
8. View the report:
   `allure serve allure-results`

## Project Areas

* Authentication and JWT security
* Smart-meter information and operational state
* OBIS-based measurement data
* Meter events and alarms
* User task handling
* Communication configuration
* MySQL database validation
* REST API testing
* Automated regression testing with PyTest
* Allure test reporting

## Project Architecture

`PyTest → API Client → FastAPI → JWT Authentication → API Routers → MySQL`

Automated tests validate API responses, authentication behavior, meter information, measurement data, events, task operations and consistency between API and database records.

## Learning Structure

The project is organized so that each layer can be studied independently:

`Configuration → Database → Models → Security → FastAPI → Routers → API Client → PyTest Fixtures → Automated Tests → Allure`

## Note

This project is an independent educational implementation designed to demonstrate software testing, API automation, database validation and smart-meter QA concepts.
