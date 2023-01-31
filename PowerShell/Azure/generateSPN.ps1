<#
    .SYNOPSIS
        Create Required SPN/App for Connection to CMP

    .DESCRIPTION
        This will require an account on the Master Azure account to create the necessary SPN.

    .USAGE
        1. Connect to GIT Repo
        2. Create Cypher for Azure creds as secret/AzureCSP:
            {"accounts":[{"username":"azureusername@something.onmicrosoft.com","password":"yourpassword"}]}
        3. Call Script as follows:
            Type: PowerShell Script
            Result Type: Single Value
            Execute Target: Local (Assuming pwsh and Azure CLI installed)

    .ExitCodes
        100 - Failed to connect to Master Subscription
        101 - Failed to create SPN
        102 - Failure to create Subscription Cypher
        103 - Failure to create SPN Cypher
#>

### Variables ###
$token = '<%=morpheus.apiAccessToken%>'
$morphURL = '<%=morpheus.applianceUrl%>'
$creds = '<%=cypher.read("secret/AzureCSP")%>' | ConvertFrom-Json
$SPNURL = '<%=customOptions.SPNName%>'
$Header = @{
    "Authorization" = "BEARER $token"
    }
$ContentType = 'application/json'

### Functions ###
function New-SPN ($name,$azureAppId,$azurePass,$azureTenant) {
    try {
        az login --service-principal -u $azureAppId -p $azurePass -t $azureTenant | Out-Null
    }
    catch {
          Write-Host "Failed to connect to Master Azure Subscription. $_" -ForegroundColor Red
          Exit 100
    }

    Try {
        $SPN = az ad sp create-for-rbac --name "https://$SPNName" --role Owner --years 10 --only-show-errors
    }
    Catch {
        Write-Host "Failed to create SPN. $_" -ForegroundColor Red
        Exit 101
    }

    return $SPN
}

# Create SPN
New-SPN -name $SPNName -azureAppId $creds.appId -azurePass $creds.password -azureTenant $creds.tenant

### Morpheus Cypher SPN Entry ###
# JSON Body
$SPNBody = @"
{
  'value': $SPN,
  'ttl': 0
}
"@

# Create Cypher
Try {
    Invoke-WebRequest -Method Put -Uri ($morphURL + 'api/cypher/v1/secret/' + $SPNName + '-SPN') -Headers $Header -Body $SPNBody -ContentType $ContentType | Out-Null
}
Catch {
    Write-Host "Failed to create SPN Cypher Entry. $_" -ForegroundColor Red
    Exit 103
}