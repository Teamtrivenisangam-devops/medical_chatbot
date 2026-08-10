variable "resource_group_name" {
  default     = "meddy-rg"
  type        = string
  description = "Resource group name"
}

variable "location" {
  default     = "canada central"
  type        = string
  description = "Azure region"
}

variable "admin_username" {
  default     = "azureuser"
  type        = string
  description = "VM Administrator username"
}

variable "ssh_public_key_path" {
  default     = "~/.ssh/id_rsa.pub"
  type        = string
  description = "Path to SSH public key"
}
