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
│       │   ├── test_add_contacts.py
│       │   ├── test_get_contacts.py
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