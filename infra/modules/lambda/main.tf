resource "aws_iam_role" "lambda_exec" {
  count = var.create_role ? 1 : 0
  name = "${var.function_name}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  count      = var.create_role ? 1 : 0
  role       = aws_iam_role.lambda_exec[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "lambda" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_exec[0].arn
  handler          = var.handler
  runtime          = var.runtime
  filename         = var.filename
  source_code_hash = filebase64sha256(var.filename)
  memory_size      = var.memory_size
  timeout          = var.timeout
  dynamic "environment" {
    for_each = var.table_name != null ? [1] : []
    content {
      variables = {
        TABLE_NAME = var.table_name
        HTTP_METHOD = var.http_method
        value_path = var.value_path
      }
    }
  }
}


resource "aws_iam_role_policy" "dynamodb_access" {
  count = var.table_name != null ? 1 : 0 # cria a policy apenas se table_name for != null
  role = aws_iam_role.lambda_exec[count.index].name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = "arn:aws:dynamodb:*:*:table/${var.table_name}"
      }
    ]
  })
}