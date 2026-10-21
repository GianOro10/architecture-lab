output "vpc_id" {
  description = "Platform VPC identifier."
  value       = aws_vpc.this.id
}

output "private_subnet_ids" {
  description = "Private subnet identifiers for the workload plane."
  value       = [for subnet in aws_subnet.private : subnet.id]
}

output "document_bucket_name" {
  description = "Encrypted document landing bucket."
  value       = aws_s3_bucket.documents.id
}

output "api_repository_url" {
  description = "ECR repository URL for the API image."
  value       = aws_ecr_repository.api.repository_url
}

output "kms_key_arn" {
  description = "Customer-managed encryption key ARN."
  value       = aws_kms_key.platform.arn
}
