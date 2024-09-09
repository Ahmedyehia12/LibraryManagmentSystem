resource "aws_internet_gateway" "this" {
  vpc_id = var.vpc_id

  tags = {
    Name = var.name
  }
}

output "internet_gateway_id" {
  value = aws_internet_gateway.this.id
}
