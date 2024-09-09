variable "vpc_id" {
  description = "The VPC ID to associate the route table with"
  type        = string
}

variable "cidr_block" {
  description = "The CIDR block for the route"
  type        = string
}

variable "gateway_id" {
  description = "The ID of the internet gateway to use in the route"
  type        = string
  default     = ""
}

variable "nat_gateway_id" {
  description = "The ID of the NAT gateway to use in the route"
  type        = string
  default     = ""
}

variable "name" {
  description = "Name tag for the route table"
  type        = string
}
