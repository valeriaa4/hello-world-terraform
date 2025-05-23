#recurso para criar api gateway
resource "aws_api_gateway_rest_api" "create_api" {
  name        = "create_api"
  description = "Criação da API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

#Recurso de autorização api gateway
resource "aws_api_gateway_authorizer" "apigw_authorizer" {
  name          = "apigw_authorizer"
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  type          = "COGNITO_USER_POOLS"
  provider_arns = [var.cognito_user_pool_arn]
}

resource "aws_api_gateway_resource" "api_resource" {
  parent_id   = aws_api_gateway_rest_api.create_api.root_resource_id
  path_part   = "${var.value_path}"
  rest_api_id = aws_api_gateway_rest_api.create_api.id
}

resource "aws_api_gateway_method" "api_method" {
  resource_id      = aws_api_gateway_resource.api_resource.id
  rest_api_id      = aws_api_gateway_rest_api.create_api.id
  http_method      = "${var.http_method}"
  authorization    = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.apigw_authorizer.id
}

resource "aws_api_gateway_integration" "lambda_integration" {
  http_method             = aws_api_gateway_method.api_method.http_method
  resource_id             = aws_api_gateway_resource.api_resource.id
  rest_api_id             = aws_api_gateway_rest_api.create_api.id
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "apigateway.amazonaws.com" 
  source_arn    = "${aws_api_gateway_rest_api.create_api.execution_arn}/*/*/*"
}

#Estagio de implantação da api
resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.create_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.api_resource.id,
      aws_api_gateway_method.api_method.id,
      aws_api_gateway_integration.lambda_integration.id
    ]))
  }


  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.lambda_integration,
    aws_lambda_permission.apigw_lambda_permission
  ]
}

resource "aws_api_gateway_stage" "api_stage" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  deployment_id = aws_api_gateway_deployment.api_deployment.id
}








