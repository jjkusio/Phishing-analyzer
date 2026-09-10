resource "azurerm_container_registry" "main" {
  name                = "jjkusioanalyzeracr"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Basic"
  admin_enabled       = false
}