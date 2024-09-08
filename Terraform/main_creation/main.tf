module "team5_vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
  name       = "team5-vpc"
}

# Public Subnet 1
module "team5_public_subnet1" {
  source                   = "./modules/subnets"
  vpc_id                   = module.team5_vpc.vpc_id
  cidr_block               = "10.0.1.0/24"
  availability_zone        = "eu-central-1a"
  map_public_ip_on_launch  = true
  name                     = "team5-public-subnet1"
}

# Public Subnet 2
module "team5_public_subnet2" {
  source                   = "./modules/subnets"
  vpc_id                   = module.team5_vpc.vpc_id
  cidr_block               = "10.0.2.0/24"
  availability_zone        = "eu-central-1b"
  map_public_ip_on_launch  = true
  name                     = "team5-public-subnet2"
}

# Private Subnet 1
module "team5_private_subnet1" {
  source                   = "./modules/subnets"
  vpc_id                   = module.team5_vpc.vpc_id
  cidr_block               = "10.0.3.0/24"
  availability_zone        = "eu-central-1a"
  map_public_ip_on_launch  = false
  name                     = "team5-private-subnet1"
}

# Private Subnet 2
module "team5_private_subnet2" {
  source                   = "./modules/subnets"
  vpc_id                   = module.team5_vpc.vpc_id
  cidr_block               = "10.0.4.0/24"
  availability_zone        = "eu-central-1b"
  map_public_ip_on_launch  = false
  name                     = "team5-private-subnet2"
}


module "team5_internet_gateway" {
  source = "./modules/igw"
  vpc_id = module.team5_vpc.vpc_id
  name   = "team5-igw"
}

module "team5_nat_gateway" {
  source    = "./modules/nat"
  subnet_id = module.team5_public_subnet1.subnet_id
  name      = "team5-nat-gateway"
}

module "team5_public_route_table" {
  source     = "./modules/route-table"
  vpc_id     = module.team5_vpc.vpc_id
  cidr_block = "0.0.0.0/0"
  gateway_id = module.team5_internet_gateway.internet_gateway_id
  name       = "team5-public-route-table"
}

module "team5_private_route_table" {
  source          = "./modules/route-table"
  vpc_id          = module.team5_vpc.vpc_id
  cidr_block      = "0.0.0.0/0"
  nat_gateway_id  = module.team5_nat_gateway.nat_gateway_id
  name            = "team5-private-route-table"
}

resource "aws_route_table_association" "team5_public_subnet_a_assoc" {
  subnet_id      = module.team5_public_subnet1.subnet_id
  route_table_id = module.team5_public_route_table.route_table_id
}

resource "aws_route_table_association" "team5_public_subnet_b_assoc" {
  subnet_id      = module.team5_public_subnet2.subnet_id
  route_table_id = module.team5_public_route_table.route_table_id
}

resource "aws_route_table_association" "team5_priv_subnet_a_assoc" {
  subnet_id      = module.team5_private_subnet1.subnet_id
  route_table_id = module.team5_private_route_table.route_table_id
}

resource "aws_route_table_association" "team5_priv_subnet_b_assoc" {
  subnet_id      = module.team5_private_subnet2.subnet_id
  route_table_id = module.team5_private_route_table.route_table_id
}


# IAM Role for EKS Cluster
resource "aws_iam_role" "eks_cluster_role" {
  name = "eks-cluster-role"

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

# Attach AmazonEC2FullAccess Policy
resource "aws_iam_role_policy_attachment" "eks_cluster_role_attach_ec2_full_access" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

# Attach AmazonEKSClusterPolicy
resource "aws_iam_role_policy_attachment" "eks_cluster_role_attach_eks_cluster_policy" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

# Attach AmazonEKSServicePolicy
resource "aws_iam_role_policy_attachment" "eks_cluster_role_attach_eks_service_policy" {
  role       = aws_iam_role.eks_cluster_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
}



# IAM Role for EKS Node Group
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

  # Attach policies for EKS node group
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  ]
}

module "eks_cluster" {
  source          = "./modules/eks"
  cluster_name    = "team5-eks-cluster"
  cluster_role_arn = aws_iam_role.eks_cluster_role.arn
  subnet_ids      = [
    module.team5_public_subnet1.subnet_id,
    module.team5_public_subnet2.subnet_id,
    module.team5_private_subnet1.subnet_id,
    module.team5_private_subnet2.subnet_id
  ]
}

module "eks_node_group" {
  source           = "./modules/eks-node-group"
  cluster_name     = module.eks_cluster.cluster_name
  node_group_name  = "team5-node-group"
  node_role_arn    = aws_iam_role.team5_eks_node_role.arn
  subnet_ids       = [
    module.team5_public_subnet1.subnet_id,
    module.team5_public_subnet2.subnet_id
  ]
  desired_size     = 1
  max_size         = 1
  min_size         = 1
}
