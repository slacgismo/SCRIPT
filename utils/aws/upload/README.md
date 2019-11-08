# Upload

## Purpose
For Lambda, its `/tmp` folder only has 512MB storage and it has `15-min` execution time limitation. Therefore, when uploading raw data to S3 bucket, we need to firstly split large files into smaller ones and then upload them to S3 bucket. This folder is used to split large files into smaller ones and upload all these files into the S3 bucket

## Usage
s3 bucket name: name of the S3 bucket you want to uplaod files to  
data type: enter `commercial` or `residential`  
file type: enter `session` or `interval`  
filename: name of the file you want to upload to S3 bucket  

Enter the below command to upload files to S3 bucket
```
python3 split_and_upload_files.py {S3 bucket name} {data type} {file type} {filename}
```
For example:
```
python3 split_and_upload_files.py script.test.raw commercial session session_test.csv
```

##Note
After splitting, file `filename.csv` will be split into several files with name as `0_filename.csv`, `1_filename.csv`, `2_filename.csv`...