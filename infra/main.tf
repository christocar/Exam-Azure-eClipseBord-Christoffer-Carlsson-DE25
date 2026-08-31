terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}"
  location = var.location
}

# ACR name must be globally unique and alphanumeric only
resource "azurerm_container_registry" "acr" {
  name                = "acr${var.project_name}${var.unique_suffix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

# the server that the web apps run on, shared between backend and frontend
resource "azurerm_service_plan" "plan" {
  name                = "asp-${var.project_name}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "backend" {
  name                = "app-${var.project_name}-backend-${var.unique_suffix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.plan.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      docker_image_name   = "eclipsebord-backend:v1"
      docker_registry_url = "https://${azurerm_container_registry.acr.login_server}"

      docker_registry_username = azurerm_container_registry.acr.admin_username
      docker_registry_password = azurerm_container_registry.acr.admin_password
    }
  }

  # Azure needs to know which port the container listens on
  app_settings = {
    WEBSITES_PORT = "8000"
  }
}