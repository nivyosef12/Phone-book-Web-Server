# Phone-book-Web-Server
A scalable and simple phone book API built with FastAPI, Postgres db, and Docker, providing CRUD operations for managing contacts. The API supports pagination, contact search, error handling, and testing.

## Features:
- Add, edit, delete, and search contacts
- Pagination support for retrieving up to 10 contacts at a time
- Dockerized setup for easy deployment
- Postgres db as the database

## Tech Stack:
- FastAPI
- Postgres db
- Docker & Docker Compose

## Server Structure
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── contacts
│   │   │   ├── services
│   │   │   │   ├── AddContant.py
│   │   │   │   ├── DeleteContant.py
│   │   │   │   ├── EditContant.py
│   │   │   │   ├── GetContant.py
│   │   │   │   ├── SearchContant.py
│   │   │   │   └── __init__.py
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   └── utils.py
│   │   ├── metrics
│   │   │   ├── services
│   │   │   │   └── __init__.py
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py
│   │   │   ├── schemas.py
│   │   │   └── utils.py
│   ├── common
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── exceptions.py
│   │   ├── logger.py
│   │   └── utils.py
│   └── middlewares
│       └── __init__.py
├── init_db
│   └── init.sql
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   └── app_tests
│       ├── __init__.py
│       ├── common_tests
│       │   ├── __init__.py
│       │   └── test_utils.py
│       ├── endpoints_tests
│       │   ├── __init__.py
│       │   ├── test_search_contacts.py
│       │   ├── test_get_contacts.py
│       │   ├── test_add_contact.py
│       │   ├── test_editcontact.py
│       │   ├── test_delete_contact.py
│       │   └── test_root.py
│       └── validator_tests
│           ├── __init__.py
│           └── test_validators.py
├── __init__.py
├── .env
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt


# Setup and Run Instructions

## 1. Clone the Repository
https://github.com/nivyosef12/Phone-book-Web-Server.git

## 2. Navigate to project dir
cd Phone-book-Web-Server

## 3. Create and Activate the Virtual Environment
- create the virtual env with: python3 -m venv phone_book_server_env  
- activate the vertual env with: source phone_book_server_env/bin/activate   
- install requirements file with: pip install -r requirements.txt  

## 4. Run Server and DB Inside a Container
- docker-compose up --build -d
- docker-compose down # to stop the container
- Navigate to http://127.0.0.1:8000/docs for simple way to test/use the server

# Run Tests
- docker-compose up --build -d
- docker exec -it phonebook-web-server /bin/sh
- pytest tests/ # to run all tests
- pytest pytest path/to/test/file # to run all tests on a certin test file (example - pytest tests/app_tests/common_tests/test_utils.py)
- docker-compose down


# Contact API Docs

# Endpoints
## Add Contact
Adds a new contact to the database.
## Endpoint: POST /add
## Request Body:
{
  "first_name": "string",
  "phone_number": "string",
  "last_name": "string (optional)",
  "address": "string (optional)"
}

## Response:
- Status Code: 201 (Success)
- Content: JSON response with operation result

## Edit Contact
Modifies an existing contact in the database.

## Endpoint: POST /edit
## Request Body:
{
  "phone_number": "string",
  "new_phone_number": "string (optional)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "address": "string (optional)"
}

## Response:
- Status Code: 200 (Success)
- Content: JSON response with operation result

## Delete Contact
Removes a contact from the database.

## Endpoint: POST /delete
## Request Body:
{
  "phone_number": "string (optional)",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}

## Response:
- Status Code: 200 (Success)
- Content: JSON response with operation result

## Search Contact

Searches for contacts in the database based on provided criteria.
## Endpoint: GET /search
## Query Parameters:
- phone_number: string (optional)
- first_name: string (optional)
- last_name: string (optional)

## Response:
- Status Code: 200 (Success)
- Content: JSON response with operation result

## Get Contact

Gets contacts from the database with a maximum of 10 with a pagination feature.
## Endpoint: GET /get
## Query Parameters:
- limit: int
- offset: int (optional)

## Response:
- Status Code: 200 (Success)
- Content: JSON response with operation result


# Error Handling
All endpoints handle errors and return appropriate HTTP status codes:
- 400: Bad Request (e.g., missing required fields)
- 404: Value error (e.g., contact not found)
- 409: Conflict error (e.g., violating db unique constraint)
- 422: Unprocessable Entity (e.g., invalid input data)
- 500: Internal Server Error