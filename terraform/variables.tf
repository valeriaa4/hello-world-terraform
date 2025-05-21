variable "runtime" {
  type = string
  default = "python3.12"
}

variable "memory_size" {
  type = number
  default = 256
}

variable "timeout" {
  type = number
  default = 20
}

variable "table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
  default     = null
}


# NOVAS VARIÁVEIS PARA COGNITO
variable "user_pool_name" {
  description = "Nome do Cognito User Pool"
  type        = string
  default     = "market-user-pool"
}

variable "app_client_name" {
  description = "Nome do Cognito App Client"
  type        = string
  default     = "market-client-app"
}


variable "user_pool_domain" {
  description = "Domínio do Cognito (subdomínio único)"
  type        = string
  default     = "market-app-demo" # subdomínio, precisa ser único na região
}
