variable "hello_function_name" {
  description = "Nome da função Lambda hello"
  type        = string
}

variable "hello_handler" {
  description = "Handler da função Lambda hello"
  type        = string
}

variable "hello_filename" {
  description = "Arquivo zip da função Lambda hello"
  type        = string
}

variable "create_function_name" {
  description = "Nome da função Lambda create"
  type        = string
}

variable "create_handler" {
  description = "Handler da função Lambda create"
  type        = string
}

variable "create_filename" {
  description = "Arquivo zip da função Lambda create"
  type        = string
}

variable "create_table_name" {
  description = "Nome da tabela DynamoDB usada pela função create"
  type        = string
}

variable "update_function_name" {
  description = "Nome da função Lambda create"
  type        = string
}

variable "update_handler" {
  description = "Handler da função Lambda create"
  type        = string
}

variable "update_filename" {
  description = "Arquivo zip da função Lambda create"
  type        = string
}

variable "update_table_name" {
  description = "Nome da tabela DynamoDB usada pela função create"
  type        = string
}

variable "remove_function_name" {
  description = "Nome da função Lambda remove"
  type        = string
}

variable "remove_handler" {
  description = "Handler da função Lambda remove"
  type        = string
}

variable "remove_filename" {
  description = "Arquivo zip da função Lambda remove"
  type        = string
}

variable "remove_table_name" {
  description = "Nome da tabela DynamoDB usada pela função remove"
  type        = string
}