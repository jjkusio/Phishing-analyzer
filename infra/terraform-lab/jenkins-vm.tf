resource "azurerm_public_ip" "jenkins" {
  name                = "phishing-analyzer-jenkins-pip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  allocation_method = "Static"
  sku               = "Standard"
}

resource "azurerm_network_interface" "jenkins" {
  name                = "phishing-analyzer-jenkins-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.jenkins.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.jenkins.id
  }
}

resource "azurerm_linux_virtual_machine" "jenkins" {
  name                = "phishing-analyzer-jenkins-vm"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_B2s"
  admin_username      = "azureuser"

  network_interface_ids = [
    azurerm_network_interface.jenkins.id
  ]

  disable_password_authentication   = true
  vm_agent_platform_updates_enabled = true
  custom_data                       = filebase64("${path.module}/cloud-init-jenkins.yaml")

  admin_ssh_key {
    username   = "azureuser"
    public_key = file(pathexpand("~/.ssh/azure_app_vm.pub"))
  }

  identity {
    type = "SystemAssigned"
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "StandardSSD_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
}