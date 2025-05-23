output "invoke_url" {
  value = "https://${aws_api_gateway_rest_api.create_api.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.api_stage.stage_name}/${var.value_path}"
}
