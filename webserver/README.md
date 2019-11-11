
# Get Started

## Prerequisites

The best way to get started is to install `docker` and `docker-compose`.
For more details, please read [Install Docker](https://docs.docker.com/v17.09/engine/installation/) and [Install Docker Compose](https://docs.docker.com/compose/install/).

## Run

Run the dockerized Django App with dockerized PostgreSQL database using:

```bash
docker-compose up
```

If you make any modification on the code, you probably need to run the following command to remove the containers and volumes and re-build the images.

```bash
docker-compose rm -f
docker-compose build
```

Then navigate to localhost:8000 on your browser.

# Development Environment Setup

Ensure you are running the anaconda `4.5.x +`

## Creating the env

```bash
conda env create -f script-environment.yml
```

If you get error installing `psycopg2`, you can probably refer to [How to install psycopg2 with “pip” on Python?](https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python).

## Updating the env after adding new packages

```bash
conda env update -f script-environment.yml
```

## Starting the env

```bash
conda activate venv_script
```

## Stopping the env

```bash
conda deactivate
```

## Setup and launch PostgreSQL

You can configure your own PostgreSQL and Django settings. However, we recommend to use dockerized PostgreSQL.

```bash
docker run -d --name my_postgres -v <path_to_save_postgres_data>:/var/lib/postgresql/data -p 5433:5432 -e POSTGRES_USER=script_admin -e POSTGRES_PASSWORD=script_passwd -e POSTGRES_DB=scriptdb postgres:9
```

Or start an existing container:

```bash
docker container start my_postgres
```

Now, you can connect to PostgreSQL via port 5433.

To stop it:

```bash
docker stop my_postgres
```

To remove the container:

```bash
docker rm /my_postgres
```

To connect to the database (you will need to install `postgresql`):

```bash
psql postgresql://script_admin:script_passwd@localhost:5433/scriptdb
```

To start the web server using the dockerized postgre:
```bash
python manage.py runserver --settings=app.settings.base
```

## Running The Project

### Migrate your models defined in Django

```bash
python manage.py makemigrations script
python manage.py migrate
```

### Start server 

```bash
./run_server
```

Then navigate to localhost:8000 on your browser.

## Unit Tests for The Project

```bash
python manage.py test --settings=app.settings.test
```
