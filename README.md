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

`pip install paramiko`

### Configure AWS

configure `variables.env`

### Run the Application

- Run with existing EC2 instance and S3 bucket: `python run.py -i <ec2_ip> -d <db_host>`
- Launch new resources and run: `python run.py`
- For more help: `python run.py --help`
