output "public_route_table_id" {
  value = aws_route_table.team5_public_rt.id
}

output "private_route_table_id" {
  value = aws_route_table.team5_private_rt.id
}
