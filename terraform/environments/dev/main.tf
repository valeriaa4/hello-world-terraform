module "lambda-um" {
  source        = "../../modules/lambda-um"
  function_name = var.hello_function_name
  handler       = var.hello_handler
  filename      = var.hello_filename
}

module "lambda-dois" {
  source         = "../../modules/lambda-dois"
  function_name  = var.create_function_name
  handler        = var.create_handler
  filename       = var.create_filename
  table_name     = var.create_table_name
}