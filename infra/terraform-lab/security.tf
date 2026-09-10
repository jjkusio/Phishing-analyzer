resource "azurerm_network_security_group" "app" {
  name                = "phishing-analyzer-app-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "allow_ssh_from_my_ip"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "37.30.46.72/32"
    destination_address_prefix = "*"
  }
  security_rule {
  name                       = "allow_ssh_from_jenkins"
  priority                   = 110
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "22"
  source_address_prefix      = azurerm_subnet.jenkins.address_prefixes[0]
  destination_address_prefix = "*"
}
security_rule {
  name                       = "allow_api_from_pc"
  priority                   = 120
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_port_range          = "*"
  destination_port_range     = "8081"
  source_address_prefix      = "37.30.46.72/32"
  destination_address_prefix = "*"
}
}

resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.main.id
  network_security_group_id = azurerm_network_security_group.app.id
}