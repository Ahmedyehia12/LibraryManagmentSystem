resource "aws_subnet" "team5_public_subnet_a" {
  vpc_id            = var.vpc_id
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.az_a
  map_public_ip_on_launch = true

  tags = {
    Name = "team5-public-subnet-a"
  }
}

resource "aws_subnet" "team5_public_subnet_b" {
  vpc_id            = var.vpc_id
  cidr_block        = "10.0.2.0/24"
  availability_zone = var.az_b
  map_public_ip_on_launch = true

  tags = {
    Name = "team5-public-subnet-b"
  }
}

resource "aws_subnet" "team5_private_subnet_a" {
  vpc_id            = var.vpc_id
  cidr_block        = "10.0.3.0/24"
  availability_zone = var.az_a

  tags = {
    Name = "team5-private-subnet-a"
  }
}

resource "aws_subnet" "team5_private_subnet_b" {
  vpc_id            = var.vpc_id
  cidr_block        = "10.0.4.0/24"
  availability_zone = var.az_b

  tags = {
    Name = "team5-private-subnet-b"
  }
}
