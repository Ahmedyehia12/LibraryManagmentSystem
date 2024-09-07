terraform {
  backend "s3" {
    bucket         = "team5-terraform-state-bucket"
    key            = "terraform/state.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
