output "user_pool_id" {
  value = module.cognito.user_pool_id
}

output "user_pool_client_id" {
  value = module.cognito.user_pool_client_id
}

output "function_name" {
  value = module.hello_terraform.function_name
}

output "invoke_arn" {
  value = module.hello_terraform.invoke_arn
}


