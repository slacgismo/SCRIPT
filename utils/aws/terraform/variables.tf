variable "region" {
  default = "us-east-1"
}

variable "raw_data_bucket_name" {
  default = "script.test.lambda.raw"
}

variable "cleaned_data_bucket_name" {
  default = "script.test.lambda.clean"
}

variable "clean_interval_lambda_name" {
  default = "script_func_clean_interval"
}

variable "clean_session_lambda_name" {
  default = "script_func_clean_session"
}

variable "iam_role_name" {
  default = "script_iam_role_for_lambdas"
}

variable "db_instance" {
  default = "db.t2.micro"
}

variable "db_name" {
  default = "scriptdb"
}

variable "db_username" {
  default = "script"
}

variable "db_pwd" {
  default = "scriptscript"
}

variable "db_port" {
  default = "5432"
}
