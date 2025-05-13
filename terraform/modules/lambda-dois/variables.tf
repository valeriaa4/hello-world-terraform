variable "function_name" {}
variable "handler" {}
variable "runtime" {
  default = "java21"
}
variable "filename" {}
variable "memory_size" {
  default = 512
}
variable "timeout" {
  default = 30
}

variable "environment" {
  type = map(string)
  default = {}
}

variable "table_name" {
  description = "Nome da tabela DynamoDB usada pela função FuncaoDoisHandler"
  type        = string
}