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