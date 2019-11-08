# Terraform

## Purpose:
Used to create S3 buckets, Lambda functions and RDS database with Terraform  

Main resources include:  
- Two S3 buckets
  - S3 bucket for raw data files
  - S3 bucket for cleaned data files
- Two Lambda functions
  - For cleaning interval files
  - For cleaning session files
- One RDS postgreSQL database

## Usage:

### Dependency:
- AWS Account
- AWS cli installed
- Terraform installed (Version: Terraform v0.12.8)

### Command:
- First edit variables (we've set default values for these variables, please reset them) in file `variables.tf` to name your AWS resources, e.g. S3 bucket, Lambda functions, RDS database' username and password...
- Set up your AWS confidential with command `aws configure`, then enter your access key ID, access secrete and region information
- Run `terraform init` and then `terraform apply` to launch these AWS resources
- Wait for it to finish and it will print out information like below about your RDS database for connection purpose

```
Outputs:
script_postgresql_db_host = XXXX
script_postgresql_db_name = XXXX
script_postgresql_db_port = XXXX
script_postgresql_db_username = XXXX
```

## Note:

### S3 bucket structure:
Below is the structure for S3 bucket storing raw data

```
S3 bucket name/
    interval/                  ---- store interval files
        commercial/            ---- store commercial files
                    filename0.csv
                    filename1.csv
                    ...
        residential/           ---- store residential files
                    filename2.csv
                    filename3.csv
                    ...
    session/                   ---- store session files
        commercial/            ---- store commercial files
                    filename4.csv
                    filename5.csv
                    ...
        residential/           ---- store residential files
                    filename6.csv
                    filename7.csv
                    ...
```

Below is the structure for S3 bucket storing cleaned data
```
S3 bucket name/
    interval/                  ---- store interval files
        commercial/            ---- store commercial files
                    cleaned_filename0.csv
                    cleaned_filename1.csv
                    ...
        residential/           ---- store residential files
                    cleaned_filename2.csv
                    cleaned_filename3.csv
                    ...
    session/                   ---- store session files
        commercial/            ---- store commercial files
                    cleaned_filename4.csv
                    cleaned_filename5.csv
                    ...
        residential/           ---- store residential files
                    cleaned_filename6.csv
                    cleaned_filename7.csv
                    ...
```

### How to trigger Lambda functions to clean files and store these cleaned files:
When you upload any `.csv` file into the S3 bucket storing raw data under `interval/commercial/`, `interval/residential/`, `session/commercial/` or `session/residential/` path, related Lambda functions will be triggered to clean the file you upload and then upload the cleaned file to the S3 bucket storing cleaned data under related path  

For example:  
When you upload file `session_test.csv` to the S3 bucket storing raw data under `session/commercial/` path, Lambda function for cleaning session file will be triggered and the cleaned file will be uploaded to the S3 bucket storing cleaned data under `session/commercial/` path  

You don't have to manually upload your files to S3 buckets, you can use a script provided by us to upload your files (for the script, refer to `upload` folder)