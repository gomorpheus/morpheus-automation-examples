#!/usr/bin/env pwsh
pwsh -c - <<'EOF'

#
    .SYNOPSIS
        Enable/Disable Amazon Plans in Bulk.

    .DESCRIPTION
        This will bulk enable and disable plans for Amazon.
        This can easily be rescoped for any cloud type or all cloud types as well.
        Run this as a task and define the code for the plans you would like enabled.
#>

#-----------------------------------------------------------------------------------------#
### Variables
$bearer = '<%=cypher.read("secret/Bearer")%>'
$morphUrl = '<%=morpheus.applianceUrl%>'
$plansApi = 'api/service-plans/'
$provisionApi = 'api/provision-types'
$morphHeader = @{
    "Authorization" = "BEARER $bearer"
    }
#-----------------------------------------------------------------------------------------#
### Enabled Plans
# $enabledPlans = (code1,code3,code8)
$enabledPlans = ('amazon-t2.nano','amazon-t2.micro')
#-----------------------------------------------------------------------------------------#

### Functions ###
function Get-TimeStamp {    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)    
}    

# Get Provision Types
$amazonProvisionType = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $provisionApi + '?name=Amazon') -Headers $morphHeader).content | convertfrom-json | select -ExpandProperty provisionTypes

# Get Amazon Plans
$amazonPlans = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $plansApi + '?includeZones=true&includeInactive&max=10000&provisionTypeId=' + $amazonProvisionType.id) -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty servicePlans

# Deactivate Plans
foreach ($amazonPlan in $amazonPlans) {
    if ($enabledPlans -notcontains $amazonPlan.code) {
        # Deactivate Plan
        Write-Host "Deactivating Service Plan $($amazonPlan.name)..."
        Invoke-WebRequest -Method Put -Uri ($morphUrl + $plansApi + $amazonPlan.id + '/deactivate') -Headers $morphHeader
    }
}

# Activate Plans
foreach ($enablePlan in $enabledPlans) {
    $plan = $amazonPlans | where code -eq $enablePlan
    # Activate Plan
    Write-Host "Activating Service Plan $($plan.name)..."
    Invoke-WebRequest -Method Put -Uri ($morphUrl + $plansApi + $plan.id + '/activate') -Headers $morphHeader
}

EOF