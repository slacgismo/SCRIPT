
# Get Started

## Prerequisites

The best way to get started is to install `docker` and `docker-compose`.
For more details, please read [Install Docker](https://docs.docker.com/v17.09/engine/installation/) and [Install Docker Compose](https://docs.docker.com/compose/install/).

## Run

Run the dockerized Django App with dockerized PostgreSQL database using:

```bash
docker-compose up
```

If you make any modification on the code, you probably need to run the following command to re-build the images.

```bash
docker-compose build
```

Then navigate to localhost:8000 on your browser.

# Development Environment Setup

Ensure you are running the anaconda `4.5.x +`

## Creating the env

```bash
conda env create -f script-environment.yml
```

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

## Running The Project

```bash
cd script
python manage.py runserver --settings=app.settings-dev
```

Then navigate to localhost:8000 on your browser.
