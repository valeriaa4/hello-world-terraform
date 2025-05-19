variable "function_name" {
  type = string
}

variable "handler" {
  type = string
}

variable "runtime" {
  type = string
  default = "python3.12"
}

variable "filename" {
  type = string
}

variable "source_code_hash" {
  type = string
}

variable "memory_size" {
  type = number
  default = 256
}

variable "timeout" {
  type = number
  default = 20
}

variable "environment" {
  type = map(string)
  default = {}
}

variable "table_name" {
  type    = string
  default = null
}