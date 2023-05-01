<#
    .SYNOPSIS
        Enable/Disable Amazon or Azure Plans in Bulk.

    .DESCRIPTION
        This will bulk enable and disable plans for Amazon.
        This can easily be rescoped for any cloud type or all cloud types as well.
        Run this as a task and define the code for the plans you would like enabled.
#>

#-----------------------------------------------------------------------------------------#
### Variables
$bearer = '<%=morpheus.apiAccessToken%>'
$morphUrl = '<%=morpheus.applianceUrl%>'
$plansApi = 'api/service-plans/'
$provisionApi = 'api/provision-types'
$morphHeader = @{
    "Authorization" = "BEARER $bearer"
    }
#-----------------------------------------------------------------------------------------#
### Enabled Plans
# $enabledPlans = (code1,code3,code8)
$enabledAmazonPlans = ('amazon-t2.nano','amazon-t2.micro')
$enabledAzurePlans = ('')
#-----------------------------------------------------------------------------------------#

### Functions ###
function Get-TimeStamp {    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)    
}    

# Get Provision Types
$amazonProvisionType = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $provisionApi + '?name=Amazon') -Headers $morphHeader).content | convertfrom-json | select -ExpandProperty provisionTypes
$azureProvisionType = = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $provisionApi + '?name=Azure') -Headers $morphHeader).content | convertfrom-json | select -ExpandProperty provisionTypes

# Get Plans
$amazonPlans = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $plansApi + '?includeZones=true&includeInactive&max=-1&provisionTypeId=' + $amazonProvisionType.id) -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty servicePlans
$azurePlans = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $plansApi + '?includeZones=true&includeInactive&max=-1&provisionTypeId=' + $azureProvisionType.id) -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty servicePlans

# Amazon Plans
    if($enabledAmazonPlans) {
        # Deactivate Amazon Plans
        foreach ($amazonPlan in $amazonPlans) {
            if ($enabledAmazonPlans -notcontains $amazonPlan.code) {
                # Deactivate Plan
                Write-Host "Deactivating Service Plan $($amazonPlan.name)..."
                Invoke-WebRequest -Method Put -Uri ($morphUrl + $plansApi + $amazonPlan.id + '/deactivate') -Headers $morphHeader
            }
        }

        # Activate Amazon Plans
        foreach ($enablePlan in $enabledAmazonPlans) {
            $plan = $amazonPlans | where code -eq $enablePlan
            # Activate Plan
            Write-Host "Activating Service Plan $($plan.name)..."
            Invoke-WebRequest -Method Put -Uri ($morphUrl + $plansApi + $plan.id + '/activate') -Headers $morphHeader
        }
    }

# Azure Plans
    if($enabledAzurePlans) {
        # Deactivate Azure Plans
        foreach ($azurePlan in $azurePlans) {
            if ($enabledAzurePlans -notcontains $azurePlan.code) {
                # Deactivate Plan
                Write-Host "Deactivating Service Plan $($azurePlan.name)..."
                Invoke-WebRequest -Method Put -Uri ($morphUrl + $plansApi + $azurePlan.id + '/deactivate') -Headers $morphHeader
            }
        }

        # Activate Azure Plans
        foreach ($enablePlan in $enabledAzurePlans) {
            $plan = $azurePlans | where code -eq $enablePlan
            # Activate Plan
            Write-Host "Activating Service Plan $($plan.name)..."
            Invoke-WebRequest -Method Put -Uri ($morphUrl + $plansApi + $plan.id + '/activate') -Headers $morphHeader
        }
    }