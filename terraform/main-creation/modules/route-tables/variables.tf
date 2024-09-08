variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "internet_gateway_id" {
  description = "The ID of the Internet Gateway"
  type        = string
}

variable "nat_gateway_id" {
  description = "The ID of the NAT Gateway"
  type        = string
}

variable "public_subnet_a_id" {
  description = "The ID of Public Subnet A"
  type        = string
}

variable "public_subnet_b_id" {
  description = "The ID of Public Subnet B"
  type        = string
}

variable "private_subnet_a_id" {
  description = "The ID of Private Subnet A"
  type        = string
}

variable "private_subnet_b_id" {
  description = "The ID of Private Subnet B"
  type        = string
}
