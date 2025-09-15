terraform {
	required_providers {
		aws = {
			source = "hashicorp/aws"
			version = "~> 5.0"
			}
		}
	required_version = ">= 1.5.0"
}

provider "aws" {
	region = "ap-southeast-2"
}

resource "aws_s3_bucket" "app_bucket" {
	bucket = "pictures-bucket-cab432-assignment"
}




