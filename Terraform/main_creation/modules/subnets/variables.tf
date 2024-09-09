variable "vpc_id" {
  description = "The VPC ID to associate the subnet with"
  type        = string
}

variable "cidr_block" {
  description = "The CIDR block for the subnet"
  type        = string
}

variable "availability_zone" {
  description = "The Availability Zone for the subnet"
  type        = string
}

variable "map_public_ip_on_launch" {
  description = "Whether to assign a public IP address to instances launched in this subnet"
  type        = bool
  default     = false
}

variable "name" {
  description = "Name tag for the subnet"
  type        = string
}
