terraform {
  backend "s3" {
    bucket         = "team5-terraform-state-bucket"  # Updated bucket name
    key            = "terraform/state.tfstate"            # Path in the bucket
    region         = "eu-central-1"                       # Replace with your region
    encrypt        = true                                 # Encrypt the state file
    dynamodb_table = "terraform-locks"                    # DynamoDB table for state locking
  }
}