output "vpc_id" {
  value = module.vpc.vpc_id
}

output "cluster_name" {
  value = module.eks_cluster.cluster_name
}

output "node_group_name" {
  value = module.eks_node_group.node_group_name
}
