
# Get Started

## Prerequisites

1. Install `docker`. For more details, please refer to [Install Docker](https://docs.docker.com/v17.09/engine/installation/).
2. Ensure you are running the anaconda `4.5.x +`.

## Development Environment Setup

### Create the env

```bash
conda env create -f script-environment.yml
```

If you get error installing `psycopg2`, you can probably refer to [How to install psycopg2 with “pip” on Python?](https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python).

To update the env after adding new packages:

```bash
conda env update -f script-environment.yml
```

### Activate the env

```bash
conda activate venv_script
```

To deactivate the env:

```bash
conda deactivate
```

### Set up PostgreSQL

You can configure your own PostgreSQL and Django settings. However, we recommend to use dockerized PostgreSQL and follow the following steps.

1. create a docker volume named `script_volume`

```bash
docker volume create script_volume
```

You can list all volumes using `docker volume ls` and delete a volume using `docker volume rm <volume-name>`.

2. start a new container:

```bash
docker run -d --name my_postgres -v script_volume:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=script_admin -e POSTGRES_PASSWORD=script_passwd -e POSTGRES_DB=scriptdb postgres:9
```

Or start an existing container:

```bash
docker container start my_postgres
```

To see all running containers:

```bash
docker ps
```

To stop it:

```bash
docker stop my_postgres
```

To remove the container:

```bash
docker rm my_postgres
```

3. (Optionally) Now, you can connect to PostgreSQL via port 5433 using shell.

To connect to the database (you will need to install `postgresql`):

```bash
psql postgresql://script_admin:script_passwd@localhost:5432/scriptdb
```

## Run The Project for Development

### Migrate the models defined in Django

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start server 

```bash
python manage.py runserver --settings=app.settings.base
```

Then navigate to `localhost:8000/api` on your browser to check available REST APIs.

## Run Unit Tests for The Project

1. Start a new PostgreSQL container

```bash
docker run --name test_postgres -p 5433:5432 -d postgres:9
```

2. Initialize the database

```bash
python manage.py makemigrations script --settings=app.settings.test
python manage.py migrate --settings=app.settings.test
```

3. Run the tests

```bash
python manage.py test --settings=app.settings.test
```
