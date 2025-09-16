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
  profile = "main"
}

resource "aws_s3_bucket" "app_bucket" {
	bucket = "pictures-bucket-cab432-assignment"
}

resource "aws_cognito_user_pool" "whiteboard_pool" {
  name = "whiteboard-user-pool"

  auto_verified_attributes = ["email"]
}

resource "aws_cognito_user_pool_client" "whiteboard_client" {
  name         = "whiteboard-client"
  user_pool_id = aws_cognito_user_pool.whiteboard_pool.id
  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]
}



resource "aws_instance" "deccl4-assignment-whiteboard" {

  ami = "ami-0000000" // Hopefully stops terraform from spazzing out
  instance_type = "t3.micro"

  lifecycle {
    ignore_changes = all
  }
}







