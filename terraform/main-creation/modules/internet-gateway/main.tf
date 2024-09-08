resource "aws_internet_gateway" "team5_gateway" {
  vpc_id = var.vpc_id

  tags = {
    Name = "team5-main-igw"
  }
}
