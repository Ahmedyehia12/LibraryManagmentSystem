output "cluster_name" {
  value = aws_eks_cluster.this.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.this.endpoint
}

output "cluster_id" {
  value = aws_eks_cluster.this.id
}

output "cluster_security_group_id" {
  value = aws_security_group.this.id
}
