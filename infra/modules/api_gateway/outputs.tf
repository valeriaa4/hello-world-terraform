output "invoke_arn" {
  value = var.invoke_arn
}

output "hello_function_name" {
  description = "Nome da função Lambda Hello recebida pelo módulo"
  value       = var.hello_function_name
}
