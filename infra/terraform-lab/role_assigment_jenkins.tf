resource "azurerm_role_assignment" "jenkins_acr_push" {
    scope = azurerm_container_registry.main.id
    role_definition_name = "AcrPush"
    principal_id = azurerm_linux_virtual_machine.jenkins.identity[0].principal_id
}

resource "azurerm_role_assignment" "jenkins_acr_reader" {
    scope                = azurerm_container_registry.main.id
    role_definition_name = "Container Registry Configuration Reader and Data Access Configuration Reader"
    principal_id         = azurerm_linux_virtual_machine.jenkins.identity[0].principal_id
}

resource "azurerm_role_assignment" "app_acr_pull" {
    scope                = azurerm_container_registry.main.id
    role_definition_name = "AcrPull"
    principal_id         = azurerm_linux_virtual_machine.app.identity[0].principal_id
}