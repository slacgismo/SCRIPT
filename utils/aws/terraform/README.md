# Terraform

## Purpose:
Used to create S3 buckets, Lambda functions and RDS database with Terraform

## Usage:
- First edit variables (we've set default values for these variables, please reset them) in file `variables.tf` to name your AWS resources, e.g. S3 bucket, Lambda functions, RDS database' username and password...
- Set up your AWS confidential with command `aws configure`, then enter your access key ID, access secrete and region information
- Run `terraform init` and then `terraform apply` to launch these AWS resources
- Wait for it to finish and it will print out information like below about your RDS database for reference

```
Outputs:
script_postgresql_db_host = XXXX
script_postgresql_db_name = XXXX
script_postgresql_db_port = XXXX
script_postgresql_db_username = XXXX
```