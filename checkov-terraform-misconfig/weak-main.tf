resource "aws_s3_bucket" "open" {
  bucket = "cr-checkov-demo-open"
}

resource "aws_security_group_rule" "ssh_alt" {
  type              = "ingress"
  security_group_id = "sg-0123456789abcdef0"
  from_port         = 2222
  to_port           = 2222
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}
