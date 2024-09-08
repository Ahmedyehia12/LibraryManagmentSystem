output "nat_gateway_id" {
  value = aws_nat_gateway.team5_nat_gateway.id
}

output "eip_id" {
  value = aws_eip.team5_nat.id
}
