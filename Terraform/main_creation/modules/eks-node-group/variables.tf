variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "node_group_name" {
  description = "The name of the node group"
  type        = string
}

variable "node_role_arn" {
  description = "The ARN of the IAM role for the nodes"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs to deploy the nodes in"
  type        = list(string)
}

variable "desired_size" {
  description = "The desired number of nodes in the node group"
  type        = number
  default     = 2
}

variable "max_size" {
  description = "The maximum number of nodes in the node group"
  type        = number
  default     = 3
}

variable "min_size" {
  description = "The minimum number of nodes in the node group"
  type        = number
  default     = 1
}

variable "instance_type" {
  description = "The type of instance to use for the nodes"
  type        = string
  default     = "t3.medium"
}