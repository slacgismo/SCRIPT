# SCRIPT - Smart ChaRging Infrastructure Planning Tool

## Structure

```text
SCRIPT/
    webserver/                  ---- Django REST Framework web server
        manage.py
        app/                    ---- settings
        script/                 ---- script web app
    frontend/                   ---- React
        src/                    ---- source code
    ec2setup/                   ---- code running on EC2
    utils/                      ---- Utils which can be copied by all images during image build
        mosek/                  ---- mosek license
    variable.env                ---- Configuration for environment variables
    UploadToCounty/             ---- Includes script to populate the counties table
```

# Getting Started with SCRIPT Running Locally

## install postgres first to avoid headaches
```sh
$ brew install postgresql
```

## to start the DB server you can just:
```sh
$ brew services start postgresql
```

## to create the DB
```sh
$ createdb scriptdb
```

#### To connect to the DB - I used [TablePlus](https://tableplus.com/). Connection params for development are the postgres defaults. You can also check the settings file to find them: `webserver/app/settings/base.py`. For now just save the new connection - we will connect to it once the Django Server is running


## Creating the env - ensure you are running the anaconda `4.5.x +`
```sh
$ conda env create -f environment.yml
```

## Updating the env with latest
```sh
$ conda env update -f environment.yml
```

## Updating the environment.yml file after adding new packages locally
```sh
$ conda env export --name venv_script > environment.yml
```

## Starting the env
```sh
$ conda activate venv_script
```

## Stopping the env
```sh
$ conda deactivate
```

## Migrate the DB
```sh
$ cd webserver
$ python manage.py migrate --settings=app.settings.base
```

## Upload County Data (this part will take about 15 minutes)
```sh
$ cd UploadToCounty
$ python UploadToPostgresCountiesZips.py
```

## Install JS dependencies (make sure npm is installed)
```sh
$ cd frontend
$ yarn install
```

# Running The App (make sure venv_script env is active on all the below terminals)

## Run Django server (terminal 1)
```sh
$ cd webserver
$ python manage.py runserver --settings=app.settings.base
```

## Run Redis in another tab (terminal 2)
```sh
$ cd webserver
$ redis-server
```

## Run celery in another tab (terminal 3)
```sh
$ cd webserver
$ celery -A app worker --loglevel=INFO
```

## Run flower in another tab (terminal 4)
```sh
$ cd webserver
$ flower -A app --port=5555
```

## Start JS server (terminal 5)
```sh
$ cd frontend
$ yarn start
```

### Note: Make sure your aws credentials are configured in your local machine
### Note: If you run into errors when getting started, attempting to install dependencies individually might lead to breakage due to inconsistencies in versioning. Your best option would be to remove conda env and recreate it with the existing environment.yml filter.
