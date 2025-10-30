resource "aws_db_subnet_group" "default" {
  name       = "analytics-db-subnet"
  subnet_ids = [aws_subnet.public1.id, aws_subnet.public2.id]
}

resource "aws_db_instance" "analytics_postgres" {
  db_name           = "events"    # <-- this is the correct argument
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  username          = "postgres"
  password          = "your-secure-password"
  allocated_storage = 20
  vpc_security_group_ids = [module.eks.cluster_security_group_id]
  db_subnet_group_name   = aws_db_subnet_group.default.name
  skip_final_snapshot    = true
}
