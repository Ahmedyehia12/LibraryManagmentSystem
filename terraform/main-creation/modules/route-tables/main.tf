resource "aws_route_table" "team5_public_rt" {
  vpc_id = var.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = var.internet_gateway_id
  }

  tags = {
    Name = "team5-public-route-table"
  }
}

resource "aws_route_table" "team5_private_rt" {
  vpc_id = var.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = var.nat_gateway_id
  }

  tags = {
    Name = "team5-private-route-table"
  }
}

resource "aws_route_table_association" "public_subnet_a_assoc" {
  subnet_id      = var.public_subnet_a_id
  route_table_id = aws_route_table.team5_public_rt.id
}

resource "aws_route_table_association" "public_subnet_b_assoc" {
  subnet_id      = var.public_subnet_b_id
  route_table_id = aws_route_table.team5_public_rt.id
}

resource "aws_route_table_association" "private_subnet_a_assoc" {
  subnet_id      = var.private_subnet_a_id
  route_table_id = aws_route_table.team5_private_rt.id
}

resource "aws_route_table_association" "private_subnet_b_assoc" {
  subnet_id      = var.private_subnet_b_id
  route_table_id = aws_route_table.team5_private_rt.id
}
