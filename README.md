# SCRIPT - Smart ChaRging Infrastructure Planning Tool

## Structure

```text
SCRIPT/
    webserver/                  ---- Django REST Framework web server
        Dockerfile
        manage.py
        app/                    ---- settings
        script/                 ---- script web app
    frontend/                   ---- React
        Dockerfile
        src/                    ---- source code
    s3watch/                    ---- Watch the algorithm results, trigger endpoint to update db
    ec2setup/                   ---- code running on EC2
    utils/                      ---- Utils which can be copied by all images during image build
        aws/
            terraform/          ---- terraform configuration
        upload/                 ---- shell/python script to split raw data and upload
        mosek/                  ---- mosek license
    docker-compose.yml          ---- Docker compose config
    variable.env                ---- Configuration for environment variables
    run.py                      ---- One-key script to start the whole project
```

## Get SCRIPT Running Locally
I used anaconda to manage my environment. However, you can easily replicate this with virtualenv. Docker instructions are below...
```bash
# install postgres first to avoid headaches
brew install postgresql
# to start the DB you can just:
brew services start postgresql

# create the needed environemnt
conda create -n venv_script python=3.7
conda activate venv_script
# install the backend dependencies
cd webserver
pip install -r requirements.txt
# other parts of the project requires other dependencies....
# instead of going through them and figuring out that you need those dependencies
# when your code breaks, just install them now:
pip install celery pandas cvxpy sklearn
# install the frontend dependencies
cd ../frontend
yarn install
```

Make sure you have postgres installed locally.

Create a database named `scriptdb` - I used [TablePlus](https://tableplus.com/) to create a DB with that name on my `localhost`. You can easily achieve the same thing via the cmd line. Also, connection params for development are the postgres defaults. You can also check the settings file to find them: `webserver/app/settings/base.py`

```bash
# migrate the DB
cd webserver
python manage.py migrate --settings=app.settings.base
```

Running the project:
```bash
cd webserver
# project assumes localhost:8000 - which should be the default
python manage.py runserver --settings=app.settings.base
cd ../frontend
yarn start 
```

Your browser should launch automatically and point to `localhost:3000`



---
## (OLD) How To Run

### Install Docker

1. install `docker` and `docker-compose`

### Install Terraform and Configure AWS

1. install `aws cli` and `terraform`
2. configure `./variables.env` and please make sure the resource names will not conflict with existing resources

### Generate Key Pair

1. generate ssh key pair(pem) with the key name of `script` and download the key
2. copy it to `./utils/aws/terraform/`
3. enter `./utils/aws/terraform/` and run `chmod 400 script.pem`

### Set Up Python Environment

1. `pip install paramiko`
2. `pip install pytz`

### Run the Application

- Run with existing AWS resources which are properly configured
  - Configure `./variables.env` with existing resources
  - EC2 instance and S3 bucket: `python run.py -i <ec2_ip> -d <db_host>`
- Launch new resources and run: `python run.py`
- For more help: `python run.py --help`
