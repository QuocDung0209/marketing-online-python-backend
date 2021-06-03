# FastAPI Server for marketing online project

## Change the password of a PostgreSQL user, you use the ALTER ROLE statement as follows:

```php
ALTER ROLE username   
WITH PASSWORD 'password';
```

**In this statement, to change the password of a user:**
- First, specify the username who you want to change the password.
- Second, provide the new password wrapped within single quotes (‘).

**Example:**
> ALTER ROLE super WITH PASSWORD 'secret123';

**Reference**: [Change the password of a PostgreSQL user](https://www.postgresqltutorial.com/postgresql-change-password/)


## Install FastAPI and other dependencies

1. **FastAPI** - this goes without saying 🙂
2. **SQLAlchemy** Object Relational Mapper (ORM)
3. **psycopg2-binary** PostgreSQL database adapter
4. **Uvicorn** a lightning-fast ASGI server

*We will also install the following development dependencies, mainly to maintain code quality and for testing.*

1. **pytest** testing framework
2. **Mypy** static type checker for Python
3. **sqlalchemy**-stubs Mypy plug-in and type stubs for SQLAlchemy
4. **Flake8** for code linting
5. **autoflake** removes unused imports and unused variables
6. **isort** sort import statements
7. **black** Python code formatter


## Generate migration file ✨

+ Create a file .py in app/models to create table on PostgreSQL on database
+ Create a file .py in app/schemas to define class to interact with table in database
+ Create a file .py in app/crud to interact with table in database

- Generate our first migraion script.
> alembic revision --autogenerate -m "Create posts table"

*This will generate a new migration file in the migrations/versions/ directory.*

- To run this migration now all we need to do is run the following command.
> alembic upgrade head ---> This will create table

- We can also roll back changes by running the below.
> alembic downgrade head

## Send email
* Change Mail server configuration in `app/core/config.py`
* Turn on the [App access is less secure](https://myaccount.google.com/u/1/lesssecureapps) for mail (if you use Gmail).

## Run project
**On Linux**
* Activate `Virtual Environment` with command:
    ```php
  poetry shell
  ```
* Use commands on `Makefile`:
    ```php
    make run # Run project
    make format # Format code
    make format-import # Format import
    make git-log # View git graph
    ```
