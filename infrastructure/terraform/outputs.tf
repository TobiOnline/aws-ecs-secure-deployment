output "repository_url" {
  value     = aws_ecr_repository.app.repository_url
  sensitive = true
}
output "github_role_arn" {
  value     = var.enable_github_oidc ? aws_iam_role.github[0].arn : null
  sensitive = true
}
output "deployment_enabled" {
  value = var.enable_deployment
}
