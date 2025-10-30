terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = ">= 2.0"
    }
  }
  required_version = ">= 1.0"
}


resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  # Enable DNS support (required for EKS)
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true
}

# Create Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create Route Table for public subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

# Associate route table with public subnets
resource "aws_route_table_association" "public1" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.30.3"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"
  vpc_id          = aws_vpc.main.id
  subnet_ids      = [aws_subnet.public1.id, aws_subnet.public2.id]

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]
      desired_size   = 1
      min_size       = 1
      max_size       = 1
    }
  }
}
