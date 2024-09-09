resource "aws_security_group" "private_sg" {
  name        = "private-sg"
  description = "Allow inbound SSH traffic from the public instance only"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    security_groups = [var.public_sg_id]  # Reference to the public security group
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "private-sg"
  }
}
