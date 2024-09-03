# IAM Role for EKS Node Group
resource "aws_iam_role" "eks_node1_role" {
  name = "eks-node1-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AdministratorAccess policy to the IAM Role
resource "aws_iam_role_policy_attachment" "eks_node_policy_admin" {
  role       = aws_iam_role.eks_node1_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AdministratorAccess"
}











resource "aws_eks_node_group" "team5_node_group-2" {
  cluster_name    = aws_eks_cluster.team5_eks_cluster.name
  node_group_name = "team5-node-group-2"
  node_role_arn   = aws_iam_role.eks_node1_role.arn
  subnet_ids      = [
    aws_subnet.team5_private_subnet_a.id,
    aws_subnet.team5_private_subnet_b.id,
  ]
  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }
  instance_types = ["t3.medium"]

  tags = {
    Name = "team5-node-group-2"
  }
}