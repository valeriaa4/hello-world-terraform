resource "aws_cognito_user_pool" "this" {
  name = var.user_pool_name

  username_attributes = ["email"]

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_uppercase = true
    require_lowercase = true
    require_numbers   = true
    require_symbols   = false
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }
}

resource "aws_cognito_user_pool_client" "this" {
  name         = var.user_pool_client_name
  user_pool_id = aws_cognito_user_pool.this.id
  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_CUSTOM_AUTH"
  ]

  prevent_user_existence_errors = "ENABLED"
}

# (Opcional) Hosted UI domain
resource "aws_cognito_user_pool_domain" "this" {
  count = var.enable_user_pool_domain ? 1 : 0

  domain       = var.user_pool_domain
  user_pool_id = aws_cognito_user_pool.this.id
}
