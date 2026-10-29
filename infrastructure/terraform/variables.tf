variable "region" {
  type    = string
  default = "eu-north-1"
  validation {
    condition     = var.region == "eu-north-1"
    error_message = "This reviewed learning configuration is restricted to Stockholm."
  }
}
variable "enable_deployment" {
  description = "False creates foundation only; true requires separate deployment approval."
  type        = bool
  default     = false
}
variable "image_digest" {
  description = "Immutable ECR digest; required before enabling deployment."
  type        = string
  default     = null
  validation {
    condition     = var.image_digest == null ? true : can(regex("^sha256:[0-9a-f]{64}$", var.image_digest))
    error_message = "Supply a real ECR sha256 digest."
  }
}
variable "demo_client_cidr" {
  description = "Approved operator IPv4 /32; kept out of Git and output."
  type        = string
  sensitive   = true
  default     = null
  validation {
    condition     = var.demo_client_cidr == null ? true : (can(cidrnetmask(var.demo_client_cidr)) && can(regex("/32$", var.demo_client_cidr)))
    error_message = "Demo ingress must be a single valid IPv4 /32."
  }
}
variable "enable_github_oidc" {
  description = "Explicit IAM approval required before enabling GitHub access."
  type        = bool
  default     = false
}
variable "existing_github_oidc_provider_arn" {
  description = "Reuse an existing account-wide GitHub provider when one exists; never duplicate it."
  type        = string
  default     = null
}
