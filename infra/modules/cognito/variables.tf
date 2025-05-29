variable "user_pool_name" {
  description = "Nome do User Pool"
  type        = string
}

variable "user_pool_client_name" {
  description = "Nome do App Client"
  type        = string
}

variable "enable_user_pool_domain" {
  description = "Se deve criar domínio para o Hosted UI"
  type        = bool
  default     = false
}

variable "user_pool_domain" {
  description = "Nome do domínio (prefixo) do Hosted UI"
  type        = string
  default     = ""
}
