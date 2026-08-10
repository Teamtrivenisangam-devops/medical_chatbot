output "public_ip_address" {
  value       = azurerm_public_ip.pip.ip_address
  description = "The public IP address of the deployed VM"
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "storage_primary_access_key" {
  value     = azurerm_storage_account.storage.primary_access_key
  sensitive = true
}
