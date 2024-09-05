# IAM Role for EKS Cluster
resource "aws_iam_role" "team5_eks_role" {
  name = "team5-eks-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "team5_eks_policy" {
  role       = aws_iam_role.team5_eks_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "team5_eks_service_policy" {
  role       = aws_iam_role.team5_eks_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
}

# IAM Role for EKS Worker Nodes
resource "aws_iam_role" "team5_eks_node_role" {
  name = "team5-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "team5_eks_node_policy" {
  role       = aws_iam_role.team5_eks_node_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "team5_eks_node_policy_ecs" {
  role       = aws_iam_role.team5_eks_node_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# IAM Role Policy Attachment for Administrator Access
resource "aws_iam_role_policy_attachment" "team5_eks_node_policy_admin" {
  role       = aws_iam_role.team5_eks_node_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_role_policy_attachment" "team5_eks_role_policy_admin" {
  role       = aws_iam_role.team5_eks_role.name
  policy_arn  = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# IAM Role Policy Attachment for ConfigMap Management
resource "aws_iam_policy" "team5_eks_manage_configmap" {
  name        = "team5-eks-manage-configmap"
  description = "Allows EKS cluster to manage aws-auth ConfigMap"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "kubernetes:UpdateConfigMap"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "team5_eks_manage_configmap_attachment" {
  role       = aws_iam_role.team5_eks_role.name
  policy_arn  = aws_iam_policy.team5_eks_manage_configmap.arn
}

# Security Group for EKS Cluster
resource "aws_security_group" "team5_eks_sg" {
  name        = "team5-eks-sg"
  description = "Security group for EKS cluster"
  vpc_id      = aws_vpc.team5_vpc.id

  # Allow inbound traffic for Kubernetes API
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "team5-eks-sg"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "team5_eks_cluster" {
  name     = "team5-cluster"
  role_arn  = aws_iam_role.team5_eks_role.arn
  version   = "1.30"

  vpc_config {
    subnet_ids = [
      aws_subnet.team5_private_subnet_a.id,
      aws_subnet.team5_private_subnet_b.id,
    ]
    security_group_ids = [aws_security_group.team5_eks_sg.id]
  }

  tags = {
    Name = "team5-cluster"
  }
}
