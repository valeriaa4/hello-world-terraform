terraform {
  backend "s3" {
    bucket       = "state-bucket-vast"
    key          = "state/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }
}

#config lambda hello_terraform: zip e module
data "archive_file" "hello_terraform" {
  type        = "zip"
  source_file = "../lambda/hello_terraform/lambda.py"
  output_path = "${path.module}/zip/hello_terraform.zip"
}

module "hello_terraform" {
  source           = "./modules/lambda"
  function_name    = "hello-terraform"
  value_path       = var.hello_value_path
  http_method      = var.get_http_method
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.hello_terraform.output_path
  source_code_hash = data.archive_file.hello_terraform.output_base64sha256
}

#config dynamodb
module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = var.table_name
}

# config lambda get_item: zip e module
data "archive_file" "get_itens" {
  type        = "zip"
  source_file = "../lambda/get_item/get_item.py"
  output_path = "${path.module}/zip/get_item.zip"
}

module "get_itens" {
  source           = "./modules/lambda"
  function_name    = "get_item"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.get_itens.output_path
  source_code_hash = data.archive_file.get_itens.output_base64sha256
  table_name       = var.table_name
  environment = {
    TABLE_NAME = var.table_name
  }
}
#config lambda create_item: zip e module
data "archive_file" "create_item" {
  type        = "zip"
  source_file = "../lambda/create_item/create_item.py"
  output_path = "${path.module}/zip/create_item.zip"
}

module "create_item" {
  source           = "./modules/lambda"
  function_name    = "create-item"
  handler          = "create_item.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.create_item.output_path
  source_code_hash = data.archive_file.create_item.output_base64sha256
  table_name       = var.table_name
  environment = {
    TABLE_NAME = var.table_name
  }
}

#config lambda update_item: zip e module
data "archive_file" "update_item" {
  type        = "zip"
  source_file = "../lambda/update_item/lambda.py"
  output_path = "${path.module}/zip/update_item.zip"
}

module "update_item" {
  source           = "./modules/lambda"
  function_name    = "update-item"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.update_item.output_path
  source_code_hash = data.archive_file.update_item.output_base64sha256
  table_name       = var.table_name
  environment = {
    TABLE_NAME = var.table_name
  }
}

#config lambda delete_item: zip e module
data "archive_file" "delete_item" {
  type        = "zip"
  source_file = "../lambda/delete_item/lambda.py"
  output_path = "${path.module}/zip/delete_item.zip"
}

module "delete_item" {
  source           = "./modules/lambda"
  function_name    = "delete-item"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.delete_item.output_path
  source_code_hash = data.archive_file.delete_item.output_base64sha256
  table_name       = var.table_name
  environment = {
    TABLE_NAME = var.table_name
  }
}

module "cognito" {
  source = "./modules/cognito"

  user_pool_name          = "market-user-pool"
  user_pool_client_name   = "market-client"
  enable_user_pool_domain = true
  user_pool_domain        = "market-auth-domain"
}

module "api_gateway" {
  source = "./modules/api_gateway"

  region                = var.region
  cognito_user_pool_arn = module.cognito.user_pool_arn

  # Configuração base 
  value_path    = var.post_get_value_path
  http_method   = var.get_http_method
  function_name = module.get_itens.function_name
  invoke_arn    = module.get_itens.invoke_arn

 # Configuração específica do HELLO
  hello_http_method   = var.hello_http_method
  hello_lambda_arn    = module.hello_terraform.invoke_arn
  hello_function_name = module.hello_terraform.function_name

  # Configuração específica do GET
  get_http_method   = var.get_http_method
  get_lambda_arn    = module.get_itens.invoke_arn
  get_function_name = module.get_itens.function_name

  # Configuração do POST
  post_http_method = var.post_http_method
  post_lambda_arn  = module.create_item.invoke_arn
  post_value_path  = var.post_get_value_path
}