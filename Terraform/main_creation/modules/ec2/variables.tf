variable "ami" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "subnet_id" {
  description = "The subnet ID to launch the instance in"
  type        = string
}

variable "security_group" {
  description = "The security group for the EC2 instance"
  type        = string
}

variable "name" {
  description = "Name tag for the EC2 instance"
  type        = string
}

variable "user_data" {
  description = "The user data script to run on instance launch"
  type        = string
  default     = ""
}

variable "key_name" {
  description = "RSA Key"
  type        = string
  default     = "my-key"
}