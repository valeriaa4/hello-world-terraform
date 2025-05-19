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