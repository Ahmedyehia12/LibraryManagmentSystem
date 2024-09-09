resource "aws_eks_node_group" "this" {
  cluster_name    = var.cluster_name
  node_group_name = var.node_group_name
  node_role_arn   = var.node_role_arn
  subnet_ids      = var.subnet_ids
  instance_types  = [var.instance_type]
  
  scaling_config {
    desired_size = var.desired_size
    max_size     = var.max_size
    min_size     = var.min_size
  }

  tags = {
    Name = "${var.cluster_name}-${var.node_group_name}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

output "node_group_arn" {
  value = aws_eks_node_group.this.arn
}

output "node_group_id" {
  value = aws_eks_node_group.this.id
}
