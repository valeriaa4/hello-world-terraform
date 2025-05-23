variable "region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "http_method" {
  description = "Métodos HTTP"
  type        = string
}

variable "value_path" {
  description = "value_path"
  type        = string
}

variable "invoke_arn" {
  type = string
}

variable "function_name" {
  type = string
}

variable "cognito_user_pool_arn" {
  description = "ARN do User Pool do Cognito"
  type        = string
}

