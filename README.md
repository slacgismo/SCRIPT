# SCRIPT - Smart ChaRging Infrastructure Planning Tool

## Architecture

All [algorithms](/ec2setup/algorithms/) are running on the same EC2 instance and our architecture design provides the same workflow as the description below:
1. Users run a script to split and upload raw data files to a S3 bucket;
2. iles uploaded to the S3 bucket trigger Lambda to clean the raw data and upload the cleaned files to the other S3 bucket (these cleaned files are served as inputs for our algorithms);
3. EC2 downloads cleaned files from S3 bucket as inputs to run algorithms and uploads the outputs to PostgreSQL database hosted on AWS RDS;
Users enter algorithm parameters and request results from RDS via locally hosted web interface and then front-end will visualize the results from RDS;
4. If there are no requested results stored in RDS, the web interface will request EC2 to run the corresponding algorithms based on user’s requesting inputs.
5. There are many tools and services applied in our project. To accomplish the project, we use multiple AWS resources, mainly including S3, EC2, RDS, Lambda and IAM, to compute, store and analyze the data, We also use Terraform to automate the deployment of AWS resources, React to serve as front-end, Django to work as back-end APIs and Docker/Docker-Compose to Dockerize the whole project.


![architecture](/doc/images/script-architecture.png)

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
        package.json
        src/                    ---- source code
    ec2setup/                   ---- code running on EC2
    utils/                      ---- Utils which can be copied by all images during image build
        aws/
            terraform/          ---- terraform configuration
        mosek/                  ---- mosek license
    docker-compose.yml          ---- Docker compose config
    variable.env                ---- Configuration for environment variables
    run.py                      ---- One-key script to start the whole project
```

### webserver design

Refer to [webserver](/doc/webserver.md).

### frontend design

Refer to [frontend](/doc/frontend.md).

### ec2setup design

Refer to [ec2setup](/doc/ec2setup.md).

### infrastructure design

Refer to [AWS Terraform](/doc/infrastructure.md)

## How To Run

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
