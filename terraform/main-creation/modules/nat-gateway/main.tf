resource "aws_eip" "team5_nat" {
  vpc = true
}

resource "aws_nat_gateway" "team5_nat_gateway" {
  allocation_id = aws_eip.team5_nat.id
  subnet_id     = var.public_subnet_id

  tags = {
    Name = "team5-nat"
  }
}
