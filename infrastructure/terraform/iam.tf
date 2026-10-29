locals {
  task_trust = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = {
        StringEquals = { "aws:SourceAccount" = data.aws_caller_identity.current.account_id }
        ArnLike      = { "aws:SourceArn" = "arn:${data.aws_partition.current.partition}:ecs:${var.region}:${data.aws_caller_identity.current.account_id}:*" }
      }
    }]
  })
}
resource "aws_iam_role" "execution" {
  name               = "${local.name}-execution"
  assume_role_policy = local.task_trust
}
resource "aws_iam_role_policy" "execution" {
  name = "image-pull-and-app-logs"
  role = aws_iam_role.execution.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
      { Effect = "Allow", Action = ["ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage"], Resource = aws_ecr_repository.app.arn },
      { Effect = "Allow", Action = ["logs:CreateLogStream", "logs:PutLogEvents"], Resource = "${aws_cloudwatch_log_group.app.arn}:*" }
    ]
  })
}
resource "aws_iam_role" "task" {
  name               = "${local.name}-task"
  assume_role_policy = local.task_trust
  # App needs no AWS API permissions; no policies attached.
}
resource "aws_iam_openid_connect_provider" "github" {
  count          = var.enable_github_oidc && var.existing_github_oidc_provider_arn == null ? 1 : 0
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}
locals {
  github_provider_arn = var.enable_github_oidc ? (var.existing_github_oidc_provider_arn != null ? var.existing_github_oidc_provider_arn : aws_iam_openid_connect_provider.github[0].arn) : null
}
resource "aws_iam_role" "github" {
  count = var.enable_github_oidc ? 1 : 0
  name  = "${local.name}-github"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = local.github_provider_arn }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          "token.actions.githubusercontent.com:sub" = "repo:TobiOnline@89221982/aws-ecs-secure-deployment@1437115174:ref:refs/heads/main"
        }
      }
    }]
  })
}
resource "aws_iam_role_policy" "github" {
  count = var.enable_github_oidc ? 1 : 0
  name  = "versioned-image-delivery"
  role  = aws_iam_role.github[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
      { Effect = "Allow", Action = ["ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage", "ecr:BatchGetImage", "ecr:DescribeImages", "ecr:DescribeRepositories"], Resource = aws_ecr_repository.app.arn },
      { Effect = "Allow", Action = ["ecs:DescribeServices", "ecs:UpdateService"], Resource = "arn:${data.aws_partition.current.partition}:ecs:${var.region}:${data.aws_caller_identity.current.account_id}:service/${local.name}/${local.name}" },
      { Effect = "Allow", Action = ["ecs:DescribeTaskDefinition"], Resource = "arn:${data.aws_partition.current.partition}:ecs:${var.region}:${data.aws_caller_identity.current.account_id}:task-definition/${local.name}:*" },
      # ECS RegisterTaskDefinition does not support resource-level permissions.
      { Effect = "Allow", Action = ["ecs:RegisterTaskDefinition"], Resource = "*", Condition = { StringEquals = { "aws:RequestedRegion" = var.region } } },
      { Effect = "Allow", Action = ["iam:PassRole"], Resource = [aws_iam_role.execution.arn, aws_iam_role.task.arn], Condition = { StringEquals = { "iam:PassedToService" = "ecs-tasks.amazonaws.com" } } }
    ]
  })
}
