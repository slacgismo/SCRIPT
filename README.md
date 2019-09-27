# Structure

```text
SCRIPT/
    script/                     ---- Django web server
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
