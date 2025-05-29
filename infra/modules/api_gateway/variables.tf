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

variable "get_lambda_arn" {
  type = string
}

variable "get_http_method" {
  description = "Métodos HTTP"
  type        = string
}

variable "post_http_method" {
  description = "Métodos HTTP"
  type        = string
}

variable "post_lambda_arn" {
  type = string
}

variable "post_value_path" {
  description = "post_value_path"
  type        = string
  default     = "create"
}

variable "patch_http_method" {
  type    = string
  default = "PATCH"
}

variable "patch_value_path" {
  type = string
}

variable "patch_lambda_arn" {
  type = string
}