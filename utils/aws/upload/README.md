# Upload

## Purpose:
For Lambda, its `/tmp` folder only has `512MB` storage and it has `15-min` execution time limitation. Therefore, when uploading raw data to S3 bucket, we need to firstly split large files into smaller ones and then upload them to S3 bucket  

For files, it has two types:  `interval` and `session`. `interval` and `session` files also have two data types:  `commercial` and `residential`. Therefore, we have a S3 structure like below:  
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

When uploading, you need to provide parameters (see below `Parameters` part) indicating which path should the files be uploaded to. The script in this folder is used to split large files into smaller ones and upload all these files into related S3 buckets under related paths

## Usage:

### Dependency:
- Python3 installed
- boto3 installed

### Parameters:
- s3 bucket name: name of the S3 bucket you want to uplaod files to  
- data type: enter `commercial` or `residential`  
- file type: enter `session` or `interval`  
- filename: name of the file you want to upload to S3 bucket  

### Command:
Enter the below command to upload files to S3 bucket
```
python3 split_and_upload_files.py {S3 bucket name} {data type} {file type} {filename}
```
For example:
```
python3 split_and_upload_files.py script.test.raw commercial session session_test.csv
```

By running the above command, file `session_test.csv` will be uploaded to S3 bucket `script.test.raw` under this path `session/commercial`

## Note:
After splitting, the file `filename.csv` will be split into several files with name as `0_filename.csv`, `1_filename.csv`, `2_filename.csv`...
