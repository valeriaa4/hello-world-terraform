variable "runtime" {
  type    = string
  default = "python3.12"
}

variable "memory_size" {
  type    = number
  default = 256
}

variable "timeout" {
  type    = number
  default = 20
}

variable "table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
  default     = "MARKET_LIST"
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


# NOVAS VARIÁVEIS PARA API GATEWAY
variable "get_http_method" {
  description = "Métodos HTTP"
  type        = string
  default     = "GET"
}

variable "hello_value_path" {
  description = "value_path"
  type        = string
  default     = "hello"
}

variable "hello_http_method" {
  description = "Métodos HTTP"
  type        = string
  default     = "GET"
}

variable "post_get_value_path" {
  description = "value_path"
  type        = string
  default     = "lista-tarefa"
}

variable "region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}



variable "post_http_method" {
  description = "Métodos HTTP"
  type        = string
  default     = "POST"
}

variable "gateway_lambda_config" {
  description = "Configurações para criar múltiplos caminhos/métodos para o API Gateway"
  type = map(object({
    path        = string
    http_method = string
    lambda_arn  = string
    lambda_name = string
  }))
  default = {}
}