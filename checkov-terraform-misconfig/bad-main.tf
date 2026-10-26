resource "aws_s3_bucket" "assets" {
  bucket = "cr-checkov-demo-assets"
  acl    = "public-read"
}

resource "aws_s3_bucket" "logs" {
  bucket = "cr-checkov-demo-logs"
}

resource "aws_security_group" "ssh" {
  name        = "cr-checkov-demo-ssh"
  description = "ssh access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ebs_volume" "data" {
  availability_zone = "ap-northeast-2a"
  size              = 20
}
