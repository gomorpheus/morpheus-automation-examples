<#
    .SYNOPSIS
    Scan for VMs created outside of Morpheus and assign service account management
        
    .DESCRIPTION
    This will run on a schedule and look for unmanaged VMs in vSphere.  Once found, this will assign to the correct tenant for billing/administration.    
#>

#################################################################################
### Variables
$bearer = '<%=morpheus.apiAccessToken%>'
$morphURL = '<%=morpheus.applianceUrl%>'

### Functions
function Get-TimeStamp {    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)      
}

### Variables
$ContentType = 'application/json'
$morphHeader = @{
    "Authorization" = "BEARER $bearer"
}

$cloudApi = 'api/zones/'
$groupApi = 'api/groups/'
$serverApi = 'api/servers/'
$cloudApi = 'api/zones/'
$tenantApi = 'api/accounts/'
$output = @()

#################################################################################
###  Morpheus Actions
# Morpheus Discovery
Write-Host "$(Get-TimeStamp) Generating Morpheus Variables..." -ForegroundColor Cyan
$clouds = (Invoke-WebRequest -Method Get -Uri ($morphURL + $cloudApi + '?max=10000') -SkipCertificateCheck -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty Zones
$tenants = (Invoke-WebRequest -Method Get -Uri ($morphURL + $tenantApi + '?max=10000') -SkipCertificateCheck -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty accounts | select id, name, customerNumber, accountNumber
$resourcePools = @()
$unmanagedServers = (Invoke-WebRequest -Method Get -Uri ($morphURL + $serverApi + '?managed=false&serverType=Vmware+VM&max=10000') -SkipCertificateCheck -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty servers | select id, name, resourcePoolId

# Generate Resource Pool Names and IDs
Write-Host "$(Get-TimeStamp) Looping through Resource Pools..." -ForegroundColor Cyan
foreach ($cloud in $clouds) {
    $rps = (Invoke-WebRequest -Method Get -Uri ($morphURL + $cloudApi + $cloud.id + '/resource-pools?max=10000') -SkipCertificateCheck -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty resourcePools
    foreach ($rp in $rps) {
      $pools = New-Object psobject
      $pools | add-member NoteProperty -Name id -Value $rp.id
      $pools | add-member NoteProperty -Name name -Value $rp.name
      $resourcePools += $pools
    }
}

# Lookup Unmanaged Systems and Make Managed
Write-Host "$(Get-TimeStamp) Begin Management Operations..." -ForegroundColor Cyan
foreach ($server in $unmanagedServers) {
    $out = New-Object PSObject
    $custNumber = $null
    $tenant = $null
    $custNumber = ($resourcePools | where id -EQ $server.resourcePoolId | select -ExpandProperty name).split('--')[1]

    if ($custNumber -gt 0) {
        $tenant = $tenants | where customerNumber -EQ $custNumber

        if ($tenant) {    
            # Default Management Body Payload
            $body = @"
{
    "server": {
    "account":{
        "id": $($tenant.id)
    },
    "sshPassword": "",
    "sshUsername": null
    },
    "installAgent": false
}
"@
            Write-Host "$(Get-TimeStamp) Converting $($server.name) to Managed in Tenant $($tenant.name)..."
            try {
                $error.clear()
                Invoke-WebRequest -Method Put -Uri ($morphURL + $serverApi + $server.id + '/install-agent') -SkipCertificateCheck -Headers $morphHeader -Body $Body -ContentType $ContentType | Out-Null
            } catch {
                $out | Add-Member NoteProperty Name $server.name
                $out | Add-Member NoteProperty Tenant $tenant.name
                $out | Add-Member NoteProperty RP $name
                $out | Add-Member NoteProperty Issue $_
                $output += $out 
            }
            if (!$error) {
                Write-Host "Success!" -ForegroundColor Green
            }
        } else {
            $out | Add-Member NoteProperty Name $server.name
            $out | Add-Member NoteProperty Tenant 'NOT FOUND'
            $out | Add-Member NoteProperty RP $name
            $out | Add-Member NoteProperty Issue 'Tenant Match Not Found'
            $output += $out 
        }
    } else {
        $out | Add-Member NoteProperty Name $server.name
        $out | Add-Member NoteProperty Tenant 'NOT FOUND'
        $out | Add-Member NoteProperty RP $name
        $out | Add-Member NoteProperty Issue 'Resource Pool Match Not Found'
        $output += $out 
    }
}

# Complete!
Write-Host `r`n
Write-Host "$(Get-TimeStamp) Management Workflow Has Completed!" -ForegroundColor Green

# Output Errors
Write-Host `r`n
Write-Host "$(Get-TimeStamp) The Following Errors Occurred ..." -ForegroundColor Red
Write-Host `r`n
$output