# Library Case Study

A FastAPI application with RESTful API endpoints for managing library operations.

## requirements

- Docker needs to be installed in your system.

## how to run

### application

- first source environment variables from the `.env`, (`.env` file provided in this repository is just an example, please change it according to your needs)

    `source .env`

- build the docker images

    `docker-compose build`

- run the dokcer containers

    `docker-compose up -d`

- After executing above commands you can navigate to http://localhost:8080/ to access the application docs and try endpoints yourself.

### tests

- create a virtual environment with python version 3.11, in this case `conda` will be used, but you can free to use your favorite method

    `conda create -n library_case python=3.11`

- activate the environment

    `conda activate library_case`

- install requirements

    `pip install app/requirements.txt`

- install development requirements

    `pip install app/dev-requirements.txt`

- run tests

    `pytest app/tests`

## implementation notes

### restapi

- `sqlmodel` is used to create data models and data validation.
- `fastapi` is used as api framework.
- `PostgreSQL` is used as the database.
- user authentication is added for endpoints.

### task scheduling
- `celery` and `celery-beat` is used for task scheduling.
- `send_reminder_emails_for_overdue_books()` task is implemented and scheduled to run every morning at 6:00 a.m.
- `create_weekly_report()` task implemented and scheduled to run every Monday at 1:00 a.m.
- created weekly reports can be found under the `data/reports` directory.
- `redis` is used as a broker.

### testing
- `pytest` is used to implement unit tests.
- an in memory database is created solely for testing.
- unit tests created for api endpoints.
- unit tests created for celery tasks.
