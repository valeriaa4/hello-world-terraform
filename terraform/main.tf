#config lambda hello_terraform: zip e module
data "archive_file" "hello_terraform" {
  type        = "zip"
  source_file = "../lambda/hello_terraform/lambda.py"
  output_path = "${path.module}/zip/hello_terraform.zip"
}

module "hello_terraform" {
  source           = "../infra/modules/lambda"
  function_name    = "hello-terraform"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.hello_terraform.output_path
  source_code_hash = data.archive_file.hello_terraform.output_base64sha256
}

#config dynamodb
module "dynamodb" {
  source     = "../infra/modules/dynamodb"
  table_name = "MARKET_LIST"
}

#config lambda create_item: zip e module
data "archive_file" "create_item" {
  type        = "zip"
  source_file = "../lambda/create_item/lambda.py"
  output_path = "${path.module}/zip/create_item.zip"
}

module "create_item" {
  source           = "../infra/modules/lambda"
  function_name    = "create-item"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.create_item.output_path
  source_code_hash = data.archive_file.create_item.output_base64sha256
  table_name = "MARKET_LIST"
  environment = {
    TABLE_NAME = "MARKET_LIST"
  }
}

#config lambda update_item: zip e module
data "archive_file" "update_item" {
  type        = "zip"
  source_file = "../lambda/update_item/lambda.py"
  output_path = "${path.module}/zip/update_item.zip"
}

module "update_item" {
  source           = "../infra/modules/lambda"
  function_name    = "update-item"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.update_item.output_path
  source_code_hash = data.archive_file.update_item.output_base64sha256
  table_name = "MARKET_LIST"
  environment = {
    TABLE_NAME = "MARKET_LIST"
  }
}

#config lambda delete_item: zip e module
data "archive_file" "delete_item" {
  type        = "zip"
  source_file = "../lambda/delete_item/lambda.py"
  output_path = "${path.module}/zip/delete_item.zip"
}

module "delete_item" {
  source           = "../infra/modules/lambda"
  function_name    = "delete-item"
  handler          = "lambda.lambda_handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  filename         = data.archive_file.delete_item.output_path
  source_code_hash = data.archive_file.delete_item.output_base64sha256
  table_name = "MARKET_LIST"
  environment = {
    TABLE_NAME = "MARKET_LIST"
  }
}



module "cognito" {
  source = "../infra/modules/cognito"

  user_pool_name         = "market-user-pool"
  user_pool_client_name  = "market-client"
  enable_user_pool_domain = true
  user_pool_domain        = "market-auth"
}
