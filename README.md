# SCRIPT - Smart ChaRging Infrastructure Planning Tool

## Structure

```text
SCRIPT/
    webserver/                  ---- Django web server
        Dockerfile
        manage.py
        app/
        script/                 ---- script web app
    s3watch/                    ---- Watch the algorithm results, trigger endpoint to update db
        Dockerfile
    ec2setup/                   ---- code running on EC2
        algorithms/
        controller/
    utils/                      ---- Utils which can be copied by all images during image build
        aws/                    ---- used by the web server backend and s3watch
            s3/
            ec2/
        upload/                 ---- shell/python script to split raw data and upload
        lambda/                 ---- used by Terraform
    docker-compose.yml          ---- Docker compose config
    main.tf                     ---- Terraform config
    variable.env                ---- Environment variables
```

## How To Run

### Set Up Python Environment

1. `pip install paramiko`
2. `pip install pytz`

### Configure AWS

1. configure `variables.env`
2. see [more requirements](./utils/aws/terraform/README.md) to install `docker` and `docker-compose`

## Generate Key Pair

1. generate ssh key pair(pem) with the key name of `script` and download the key
2. copy it to `./utils/aws/terraform/`
3. run `chmod 400 script.pem` in `./utils/aws/terraform/`

### Run the Application

- Run with existing EC2 instance and S3 bucket: `python run.py -i <ec2_ip> -d <db_host>`
- Launch new resources and run: `python run.py`
- For more help: `python run.py --help`
