output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "backend_url" {
  value = "https://${azurerm_linux_web_app.backend.default_hostname}"
}