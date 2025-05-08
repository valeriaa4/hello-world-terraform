module "lambda_funcao_um" {
  source        = "./modules/lambda"
  function_name = var.function_name
  handler       = var.handler
  filename      = var.filename
}

