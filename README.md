# Application Name

## Overview

- This application is a web service built using [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), and [Alembic](https://alembic.sqlalchemy.org/). It provides a robust and efficient API for Social Media Posting.

- The application is designed to handle multiple users, posts, and comments, with features for creating,
reading, updating, and deleting (CRUD) operations.

- The Application is live at [Fastapi-Socio](https://fastapi-development.onrender.com/docs)

## Features

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) system.
- **Alembic**: Database migration tool for SQLAlchemy.

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL or your preferred database
- Virtual environment tool (e.g., `venv`)

### Setup

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and activate it.
3. Install the required dependencies using `pip`.
4. Configure the necessary environment variables in a `.env` file, such as the database URL.
5. Run the database migrations using Alembic.
6. Start the FastAPI application using Uvicorn. The API will be available at `http://127.0.0.1:8000`.

## Usage

### API Endpoints

- **GET /posts/**: Fetch a list of posts.
- **POST /posts/**: Create a new post.
- **PUT /posts/{id}**: Update an existing post.
- **DELETE /posts/{id}**: Delete a post.

For detailed API documentation, visit `/docs` or `/redoc` when the application is running.

### Database Migrations

After modifying the SQLAlchemy models, create a new migration with Alembic and apply it.

## Testing

Run tests using `pytest`.

![image](https://github.com/user-attachments/assets/6aec8f0d-b345-4d55-9f8c-a40643915b80)
