variable "aws_region" {
  description = "Region for AWS resources."
  default     = "us-east-1" 
}

variable "aws_profile" {
  description = "AWS CLI profile name"
  default     = "default"
}

variable "cluster_name" {
  description = "EKS Cluster name"
  default     = "analytics-eks"
}

