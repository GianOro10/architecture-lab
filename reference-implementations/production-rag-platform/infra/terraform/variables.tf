variable "aws_region" {
  description = "AWS region used by the reference foundation."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Lowercase project identifier used in resource names."
  type        = string
  default     = "production-rag-platform"

  validation {
    condition     = can(regex("^[a-z0-9-]{3,32}$", var.project_name))
    error_message = "project_name must contain 3-32 lowercase letters, numbers or hyphens."
  }
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "stage", "prod"], var.environment)
    error_message = "environment must be dev, test, stage or prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR assigned to the platform VPC."
  type        = string
  default     = "10.40.0.0/16"
}
