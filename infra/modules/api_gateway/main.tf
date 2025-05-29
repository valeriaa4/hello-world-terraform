# recurso para criar api gateway
resource "aws_api_gateway_rest_api" "create_api" {
  name        = "create_api"
  description = "Criação da API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

#Recurso de autorização api gateway
resource "aws_api_gateway_authorizer" "apigw_authorizer" {
  name            = "apigw_authorizer"
  rest_api_id     = aws_api_gateway_rest_api.create_api.id
  type            = "COGNITO_USER_POOLS"
  provider_arns   = [var.cognito_user_pool_arn]
  identity_source = "method.request.header.Authorization"
}

# Recurso GET 
resource "aws_api_gateway_resource" "get_item_resource" {
  parent_id   = aws_api_gateway_rest_api.create_api.root_resource_id
  path_part   = "lista-tarefa"
  rest_api_id = aws_api_gateway_rest_api.create_api.id
}

resource "aws_api_gateway_method" "get_item_method" {
  resource_id   = aws_api_gateway_resource.get_item_resource.id
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  http_method   = var.get_http_method
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.apigw_authorizer.id
}

resource "aws_api_gateway_integration" "get_item_integration" {
  http_method             = aws_api_gateway_method.get_item_method.http_method
  resource_id             = aws_api_gateway_resource.get_item_resource.id
  rest_api_id             = aws_api_gateway_rest_api.create_api.id
  integration_http_method = var.get_http_method
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.get_lambda_arn}/invocations"

}

resource "aws_lambda_permission" "get_item_permission" {
  statement_id  = "AllowExecutionFromAPIGatewayGet"
  action        = "lambda:InvokeFunction"
  function_name = "get_item"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.create_api.id}/*/${var.get_http_method}/lista-tarefa"
}

resource "aws_api_gateway_resource" "api_resource" {
  parent_id   = aws_api_gateway_rest_api.create_api.root_resource_id
  path_part   = var.value_path
  rest_api_id = aws_api_gateway_rest_api.create_api.id
}

resource "aws_api_gateway_method" "api_method" {
  resource_id   = aws_api_gateway_resource.api_resource.id
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  http_method   = var.http_method
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.apigw_authorizer.id
}

resource "aws_api_gateway_integration" "lambda_integration" {
  http_method             = aws_api_gateway_method.api_method.http_method
  resource_id             = aws_api_gateway_resource.api_resource.id
  rest_api_id             = aws_api_gateway_rest_api.create_api.id
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = local.lambda_invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = "lista-tarefa"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.create_api.execution_arn}/*/*/*"
}

resource "aws_api_gateway_method" "add_item_api_method" {
  resource_id   = aws_api_gateway_resource.post_api_resource.id
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  http_method   = var.post_http_method
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.apigw_authorizer.id
}

resource "aws_api_gateway_integration" "add_item_integration" {
  http_method             = aws_api_gateway_method.add_item_api_method.http_method
  resource_id             = aws_api_gateway_resource.post_api_resource.id
  rest_api_id             = aws_api_gateway_rest_api.create_api.id
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.post_lambda_arn}/invocations"
}

resource "aws_lambda_permission" "add_item_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = "create-item"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.create_api.execution_arn}/*/*/*"
}

resource "aws_api_gateway_resource" "post_api_resource" {
  parent_id   = aws_api_gateway_rest_api.create_api.root_resource_id
  path_part   = var.post_value_path
  rest_api_id = aws_api_gateway_rest_api.create_api.id
}

# Estagio de implantação da api
resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.create_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.api_resource.id,
      aws_api_gateway_method.api_method.id,
      aws_api_gateway_integration.lambda_integration.id,
      aws_api_gateway_resource.post_api_resource.id,
      aws_api_gateway_method.add_item_api_method.id,
      aws_api_gateway_integration.add_item_integration.id,
      aws_api_gateway_resource.patch_item_resource.id,
      aws_api_gateway_method.patch_item_method.id,
      aws_api_gateway_integration.patch_item_integration.id,
      aws_api_gateway_resource.get_item_resource.id,
      aws_api_gateway_method.get_item_method.id,
      aws_api_gateway_integration.get_item_integration.id
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.lambda_integration,
    aws_lambda_permission.apigw_lambda_permission,
    aws_api_gateway_integration.patch_item_integration,
    aws_lambda_permission.patch_item_permission,
    aws_api_gateway_integration.get_item_integration,
    aws_lambda_permission.get_item_permission
  ]
}

resource "aws_api_gateway_stage" "api_stage" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  deployment_id = aws_api_gateway_deployment.api_deployment.id
}

# Rota PATCH /lista-tarefa/{item_id}
resource "aws_api_gateway_resource" "patch_api_resource" {
  parent_id   = aws_api_gateway_rest_api.create_api.root_resource_id
  path_part   = "lista-tarefa"
  rest_api_id = aws_api_gateway_rest_api.create_api.id
}

resource "aws_api_gateway_resource" "patch_item_resource" {
  parent_id   = aws_api_gateway_resource.patch_api_resource.id
  path_part   = "{item_id}"
  rest_api_id = aws_api_gateway_rest_api.create_api.id
}

resource "aws_api_gateway_method" "patch_item_method" {
  resource_id   = aws_api_gateway_resource.patch_item_resource.id
  rest_api_id   = aws_api_gateway_rest_api.create_api.id
  http_method   = var.patch_http_method
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.apigw_authorizer.id
}

resource "aws_api_gateway_integration" "patch_item_integration" {
  http_method             = aws_api_gateway_method.patch_item_method.http_method
  resource_id             = aws_api_gateway_resource.patch_item_resource.id
  rest_api_id             = aws_api_gateway_rest_api.create_api.id
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.patch_lambda_arn}/invocations"
}

resource "aws_lambda_permission" "patch_item_permission" {
  statement_id  = "AllowExecutionFromAPIGatewayPatch"
  action        = "lambda:InvokeFunction"
  function_name = "update-item"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.create_api.execution_arn}/*/*/*"
}