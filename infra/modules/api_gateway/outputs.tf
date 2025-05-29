# output "invoke_arn" {
#   value = var.invoke_arn
# }

output "invoke_arn" {
  value = aws_lambda_function.lambda.invoke_arn
}
