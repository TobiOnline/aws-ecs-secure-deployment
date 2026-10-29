terraform {
  required_version = ">= 1.17.1, < 1.18.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project   = "aws-ecs-secure-deployment"
      ManagedBy = "Terraform"
      Purpose   = "temporary-learning-demo"
    }
  }
}
