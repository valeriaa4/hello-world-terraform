# data "aws_caller_identity" "current" {}

# locals {
#   lambda_invoke_arn = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:${var.lambda_function_name}/invocations"
# }
