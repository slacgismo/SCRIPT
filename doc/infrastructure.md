# SCRIPT-infrastructure

[infrastructure using terraform](/utils/aws/terraform/README.md)

It will launch all resources in the infrastructure using `Terraform` and bootstrap the `EC2` server.

## What we have done

The `IaC` code should be able to launch all resources successfully if you can configure all environment variables correctly.

## What can be improved

1. The code of `EC2` instance bootstrapping should be modified if you decide to develop a new [ec2setup/ec2server](/doc/ec2setup.md).
