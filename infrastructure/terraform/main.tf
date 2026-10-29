locals {
  name = "aws-ecs-secure-deployment"
}
data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_vpc" "default" {
  default = true
}
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "default-for-az"
    values = ["true"]
  }
}
data "aws_subnet" "selected" {
  id = sort(data.aws_subnets.default.ids)[0]
}
resource "aws_ecr_repository" "app" {
  name                 = local.name
  image_tag_mutability = "IMMUTABLE"
  force_delete         = false
  encryption_configuration {
    encryption_type = "AES256"
  }
  image_scanning_configuration {
    scan_on_push = true
  }
}
resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Expire untagged images after one day; retain tagged rollback versions"
      selection = {
        tagStatus   = "untagged"
        countType   = "sinceImagePushed"
        countUnit   = "days"
        countNumber = 1
      }
      action = { type = "expire" }
    }]
  })
}
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${local.name}"
  retention_in_days = 1
}
resource "aws_ecs_cluster" "app" {
  name = local.name
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}
resource "aws_security_group" "app" {
  name_prefix = "ecs-demo-"
  description = "Temporary ECS demo; ingress limited to approved operator /32"
  vpc_id      = data.aws_vpc.default.id
}
resource "aws_vpc_security_group_egress_rule" "https" {
  security_group_id = aws_security_group.app.id
  description       = "ECR image layers and CloudWatch over TLS"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}
resource "aws_vpc_security_group_ingress_rule" "demo" {
  count             = var.enable_deployment ? 1 : 0
  security_group_id = aws_security_group.app.id
  description       = "Approved operator only; temporary HTTP demo with no sensitive data"
  cidr_ipv4         = var.demo_client_cidr
  ip_protocol       = "tcp"
  from_port         = 8000
  to_port           = 8000
  lifecycle {
    precondition {
      condition     = var.demo_client_cidr != null
      error_message = "Deployment requires an explicitly approved operator /32."
    }
  }
}
resource "aws_ecs_task_definition" "app" {
  count                    = var.enable_deployment ? 1 : 0
  family                   = local.name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
  container_definitions = jsonencode([{
    name                   = "app"
    image                  = "${aws_ecr_repository.app.repository_url}@${var.image_digest == null ? "MISSING" : var.image_digest}"
    essential              = true
    user                   = "10001:10001"
    readonlyRootFilesystem = true
    portMappings           = [{ containerPort = 8000, protocol = "tcp" }]
    # Fargate has no tmpfs support. Dockerfile VOLUME seeds app-owned runtime storage.
    mountPoints = [{ sourceVolume = "runtime-tmp", containerPath = "/app/runtime", readOnly = false }]
    linuxParameters = {
      capabilities       = { drop = ["ALL"] }
      initProcessEnabled = true
    }
    healthCheck = {
      command     = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]
      interval    = 15
      timeout     = 5
      retries     = 3
      startPeriod = 15
    }
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.app.name
        "awslogs-region"        = var.region
        "awslogs-stream-prefix" = "app"
      }
    }
  }])
  volume {
    name = "runtime-tmp"
  }
  lifecycle {
    precondition {
      condition     = var.image_digest != null
      error_message = "Publish and verify an ECR image digest before deployment."
    }
  }
}
resource "aws_ecs_service" "app" {
  count                              = var.enable_deployment ? 1 : 0
  name                               = local.name
  cluster                            = aws_ecs_cluster.app.id
  task_definition                    = aws_ecs_task_definition.app[0].arn
  desired_count                      = 1
  launch_type                        = "FARGATE"
  platform_version                   = "1.4.0"
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
  wait_for_steady_state              = true
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  network_configuration {
    subnets          = [data.aws_subnet.selected.id]
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = true
  }
  lifecycle {
    # After the first approved deployment, CI owns service revision updates.
    ignore_changes = [task_definition]
  }
  depends_on = [aws_iam_role_policy.execution, aws_vpc_security_group_ingress_rule.demo]
}
