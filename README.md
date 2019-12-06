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

## How To Run

### Install Docker

1. install `docker` and `docker-compose`

### Install Terraform and Configure AWS

1. install `aws cli` and `terraform`
2. configure `./variables.env` and please make sure the resource names will not conflict with existing resources

## Generate Key Pair

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
