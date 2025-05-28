output "invoke_arn" {
  value = var.invoke_arn
}

output "function_name" {
  description = "Nome da função Lambda hello"
  value       = aws_lambda_function.hello_lambda.function_name
}

output "hello_function_name" {
  description = "Nome da função Lambda Hello recebida pelo módulo"
  value       = var.hello_function_name
}
