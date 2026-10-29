resource "aws_cloudwatch_metric_alarm" "cpu" {
  count               = var.enable_deployment ? 1 : 0
  alarm_name          = "ecs-demo-high-cpu"
  alarm_description   = "CPU above 80 percent for two minutes; console alarm only, no notification destination."
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 2
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  dimensions = {
    ClusterName = aws_ecs_cluster.app.name
    ServiceName = "aws-ecs-secure-deployment"
  }
}
