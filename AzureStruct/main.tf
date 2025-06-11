variable "subscription_id" {
  type = string
}

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-proj"
  location = "uksouth"
}

resource "azurerm_cosmosdb_account" "cosmos_account" {
  name                = "accfran"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  capabilities {
    name = "EnableServerless"
  }

}

output "cosmos_primary_key" {
  value     = azurerm_cosmosdb_account.cosmos_account.primary_key
  sensitive = true
}

resource "azurerm_cosmosdb_sql_database" "cosmos_db" {
  name                = "databaseFran"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos_account.name
}

resource "azurerm_cosmosdb_sql_container" "container" {
  name                = "dados"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos_account.name
  database_name       = azurerm_cosmosdb_sql_database.cosmos_db.name
  partition_key_paths = ["/id"] # usa a mesma key que no teu backend

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }

    excluded_path {
      path = "/\"_etag\"/?"
    }
  }
}




#### Registry
resource "azurerm_container_registry" "acr" {
  name                     = "acrprojfran"           # Nome único globalmente
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Basic"                 # Pode ser Basic, Standard ou Premium
  admin_enabled            = true                    # Ativa o administrador (útil para autenticação simples)

  # Opcional, tags para organizar recursos
  tags = {
    environment = "dev"
    project     = "ProjetoLEI"
  }
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  value = azurerm_container_registry.acr.admin_username
}

output "acr_admin_password" {
  value     = azurerm_container_registry.acr.admin_password
  sensitive = true
}
