terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 3.35.0"
    }
  }
}

provider "aws" {
  region     = local.vpc_options.region
  access_key = var.access_key
  secret_key = var.secret_key

}