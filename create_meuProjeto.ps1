
Write-Output "Processo iniciado."

# Definições
$resourceGroup = "RG-Projeto"
$vmName = "Ubuntu24VM"
$location = "uksouth"
$adminUsername = "adminuser"
$password = "P@ssword1234"  # Substituir por um método seguro em produção
$size = "Standard_B2ms"  # 2 vCPU, 4GB RAM
$image = "Ubuntu2204"
$osDiskType = "StandardSSD_LRS"
$vnetName = "Ubuntu24-VNet"
$subnetName = "Ubuntu24-Subnet"
$publicIpName = "Ubuntu24-PublicIP"
$nicName = "Ubuntu24-NIC"
$securityGroupName = "Ubuntu24-NSG"
$availabilityZone = 1  # Escolher uma zona de disponibilidade
$cloudInitFile = "./cloud-init.txt"

# Criar grupo de recursos
az group create --name $resourceGroup --location $location

# Criar rede virtual e subnet
az network vnet create --resource-group $resourceGroup --name $vnetName --subnet-name $subnetName

# Criar IP público
az network public-ip create --resource-group $resourceGroup --name $publicIpName --sku Standard

# Criar grupo de segurança e regras
az network nsg create --resource-group $resourceGroup --name $securityGroupName
az network nsg rule create --resource-group $resourceGroup --nsg-name $securityGroupName --name AllowSSH --protocol Tcp --direction Inbound --priority 1000 --source-address-prefixes "*" --source-port-ranges "*" --destination-port-ranges 22 --access Allow
az network nsg rule create --resource-group $resourceGroup --nsg-name $securityGroupName --name AllowHTTP --protocol Tcp --direction Inbound --priority 1001 --source-address-prefixes "*" --source-port-ranges "*" --destination-port-ranges 80 --access Allow
az network nsg rule create --resource-group $resourceGroup --nsg-name $securityGroupName --name AllowHTTPS --protocol Tcp --direction Inbound --priority 1002 --source-address-prefixes "*" --source-port-ranges "*" --destination-port-ranges 443 --access Allow
az network nsg rule create --resource-group $resourceGroup --nsg-name $securityGroupName --name AllowPort5000 --protocol Tcp --direction Inbound --priority 1003 --source-address-prefixes "*" --source-port-ranges "*" --destination-port-ranges 5000 --access Allow

# Criar interface de rede
az network nic create --resource-group $resourceGroup --name $nicName --vnet-name $vnetName --subnet $subnetName --network-security-group $securityGroupName --public-ip-address $publicIpName


Write-Output "Git in"
$cloudInitContent = Get-Content -Path $cloudInitFile -Raw
[System.Text.Encoding]::UTF8.GetBytes($cloudInitContent) | Set-Content -Path $cloudInitFile -Encoding Byte
Write-Output "Git out"

# Criar VM
az vm create `
    --resource-group $resourceGroup `
    --name $vmName `
    --location $location `
    --size $size `
    --image $image `
    --admin-username $adminUsername `
    --admin-password $password `
    --nics $nicName `
    --os-disk-size-gb 30 `
    --storage-sku $osDiskType `
    --zone $availabilityZone `
    --custom-data $cloudInitFile

Write-Output "VM $vmName created in $location ."




#az vm image list --publisher Canonical --offer 0001-com-ubuntu-server --all --query "[?purchasePlan==null]" --output table
#az vm image list --all --publisher Canonical --offer "Ubuntu" --sku 24 --query "[?purchasePlan==null]" --output table