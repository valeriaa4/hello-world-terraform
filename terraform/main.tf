module "lambda-um" {
  source        = "./modules/lambda-um"
  function_name = var.hello_function_name
  handler       = var.hello_handler
  filename      = var.hello_filename
}

module "lambda-dois" {
  source         = "./modules/lambda-dois"
  function_name  = var.create_function_name
  handler        = var.create_handler
  filename       = var.create_filename
  table_name     = var.create_table_name
}

module "lambda-tres" {
  source         = "./modules/lambda-tres"
  function_name  = var.update_function_name
  handler        = var.update_handler
  filename       = var.update_filename
  table_name     = var.update_table_name
}

module "lambda-quatro" {
  source         = "./modules/lambda-quatro"
  function_name  = var.remove_function_name
  handler        = var.remove_handler
  filename       = var.remove_filename
  table_name     = var.remove_table_name
}