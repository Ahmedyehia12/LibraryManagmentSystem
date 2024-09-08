output "public_subnet_a_id" {
  value = aws_subnet.team5_public_subnet_a.id
}

output "public_subnet_b_id" {
  value = aws_subnet.team5_public_subnet_b.id
}

output "private_subnet_a_id" {
  value = aws_subnet.team5_private_subnet_a.id
}

output "private_subnet_b_id" {
  value = aws_subnet.team5_private_subnet_b.id
}
