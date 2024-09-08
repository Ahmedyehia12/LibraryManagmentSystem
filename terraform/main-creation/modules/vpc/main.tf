resource "aws_vpc" "team5_vpc" {
  cidr_block = var.cidr_block
  tags = {
    Name = "team5-vpc"
  }
}
