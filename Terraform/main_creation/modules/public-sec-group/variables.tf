variable "vpc_id" {
  description = "The VPC ID to associate the security group with"
  type        = string
}

variable "name" {
  description = "Name tag for the security group"
  type        = string
}

variable "description" {
  description = "Description of the security group"
  type        = string
}

variable "ssh_cidr_blocks" {
  description = "CIDR blocks for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "http_cidr_blocks" {
  description = "CIDR blocks for HTTP access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
