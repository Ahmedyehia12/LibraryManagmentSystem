variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "cluster_role_arn" {
  description = "The ARN of the IAM role for the EKS cluster"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to the EKS cluster"
  type        = map(string)
  default     = {}
}
