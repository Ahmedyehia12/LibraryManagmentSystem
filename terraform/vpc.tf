# Create the VPC
resource "aws_vpc" "team5_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "team5-vpc"
  }
}

# Create Public Subnet in Availability Zone A
resource "aws_subnet" "team5_public_subnet_a" {
  vpc_id            = aws_vpc.team5_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1a"  # Change to the correct AZ in your region
  map_public_ip_on_launch = true

  tags = {
    Name = "team5-public-subnet-a"
  }
}

# Create Public Subnet in Availability Zone B
resource "aws_subnet" "team5_public_subnet_b" {
  vpc_id            = aws_vpc.team5_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1b"  # Change to the correct AZ in your region
  map_public_ip_on_launch = true

  tags = {
    Name = "team5-public-subnet-b"
  }
}

# Create Private Subnet in Availability Zone A
resource "aws_subnet" "team5_private_subnet_a" {
  vpc_id            = aws_vpc.team5_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "eu-central-1a"  # Change to the correct AZ in your region

  tags = {
    Name = "team5-private-subnet-a"
  }
}

# Create Private Subnet in Availability Zone B
resource "aws_subnet" "team5_private_subnet_b" {
  vpc_id            = aws_vpc.team5_vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "eu-central-1b"  # Change to the correct AZ in your region

  tags = {
    Name = "team5-private-subnet-b"
  }
}

# Create the Internet Gateway
resource "aws_internet_gateway" "team5_gateway" {
  vpc_id = aws_vpc.team5_vpc.id

  tags = {
    Name = "team5-main-igw"
  }
}

# Create the NAT Gateway in Public Subnet A
resource "aws_eip" "team5_nat" {
  vpc = true
}

resource "aws_nat_gateway" "team5_nat_gateway" {
  allocation_id = aws_eip.team5_nat.id
  subnet_id     = aws_subnet.team5_public_subnet_a.id

  tags = {
    Name = "team5-nat"
  }
}

# Create Public Route Table
resource "aws_route_table" "team5_public_rt" {
  vpc_id = aws_vpc.team5_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.team5_gateway.id
  }

  tags = {
    Name = "team5-public-route-table"
  }
}

# Associate Public Subnets with Public Route Table
resource "aws_route_table_association" "team5_public_subnet_a_assoc" {
  subnet_id      = aws_subnet.team5_public_subnet_a.id
  route_table_id = aws_route_table.team5_public_rt.id
}

resource "aws_route_table_association" "team5_public_subnet_b_assoc" {
  subnet_id      = aws_subnet.team5_public_subnet_b.id
  route_table_id = aws_route_table.team5_public_rt.id
}

# Create Private Route Table
resource "aws_route_table" "team5_private_rt" {
  vpc_id = aws_vpc.team5_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.team5_nat_gateway.id
  }

  tags = {
    Name = "team5-private-route-table"
  }
}

# Associate Private Subnets with Private Route Table
resource "aws_route_table_association" "team5_private_subnet_a_assoc" {
  subnet_id      = aws_subnet.team5_private_subnet_a.id
  route_table_id = aws_route_table.team5_private_rt.id
}

resource "aws_route_table_association" "team5_private_subnet_b_assoc" {
  subnet_id      = aws_subnet.team5_private_subnet_b.id
  route_table_id = aws_route_table.team5_private_rt.id
}