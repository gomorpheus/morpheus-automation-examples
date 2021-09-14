### This script is incomplete.

### Params ###
Param (
    [Parameter(Mandatory = $true)]$bearer,
    [Parameter(Mandatory = $true)]$morphURL,
    [Parameter(Mandatory = $true)]$group,
    [Parameter(Mandatory = $true)]$cloud,
    [Parameter(Mandatory=$false)]
    [string[]]$folders=@(),
    [Parameter(Mandatory=$false)]
    [string[]]$datastores=@(),
    [Parameter(Mandatory=$false)]
    [string[]]$networks=@(),
    [Parameter(Mandatory=$false)]
    [string[]]$resourcePools=@()

)

$headers = @{
    "Authorization" = "Bearer $bearer"
    "ContentType"   = "application/json"
}

$group = (Invoke-WebRequest -Uri ($morphURL + "/api/groups?name=$($group)") -SkipCertificateCheck -Headers $headers | ConvertFrom-Json | Select-Object -ExpandProperty groups).id
$cloud = (Invoke-WebRequest -Uri ($morphURL + "/api/zones?name=$cloud") -SkipCertificateCheck -Headers $headers | ConvertFrom-Json | Select-Object -ExpandProperty zones).id


### FOLDERS

if ($folders){
    $construct = "folders"
    $object = $folders

    foreach ($item in $object) {
    # Var
    Write-Host "Modifying $($construct): $($item)" -ForegroundColor DarkCyan
    $itemGet = Invoke-WebRequest -Uri ($morphURL + "/api/zones/$($cloud)/$($construct)?name=$($item)") -SkipCertificateCheck -Headers $headers | ConvertFrom-Json | Select-Object -ExpandProperty folders
    $itemGet = $itemGet[$itemGet.count -1]
    $itemSites = $itemGet.resourcePermissions.sites
    $itemGroup = New-Object psobject
    $itemGroup | Add-Member NoteProperty -Name id -Value $group
    $itemGroup | Add-Member NoteProperty -Name default -Value True

    $itemSites += $itemGroup
    $itemSites = $itemSites | ConvertTo-Json

    $itemBody = @"
{
    "folder": {
        "resourcePermission": {
            "all": false,
            "sites": $('[' + $itemSites.TrimStart('[').TrimEnd(']') + ']')
        }
    }
}
"@

    $put = Invoke-WebRequest -Method Put -Uri ($morphURL + "/api/zones/$($cloud)/$($construct)/$($itemGet.id)") -SkipCertificateCheck -Headers $headers -Body $itemBody
}
}

### RESOURCE POOLS

if ($resourcePools){
    $construct = "resource-pools"
    $object = $resourcePools

    foreach ($item in $object) {
    # Var
    Write-Host "Modifying $($construct): $($item)" -ForegroundColor DarkCyan
    $itemGet = Invoke-WebRequest -Uri ($morphURL + "/api/zones/$($cloud)/$($construct)?name=$($item)") -SkipCertificateCheck -Headers $headers | ConvertFrom-Json | Select-Object -ExpandProperty resourcepools
    $itemGet = $itemGet[$itemGet.count -1]
    $itemSites = $itemGet.resourcePermissions.sites
    $itemGroup = New-Object psobject
    $itemGroup | Add-Member NoteProperty -Name id -Value $group
    $itemGroup | Add-Member NoteProperty -Name default -Value True

    $itemSites += $itemGroup
    $itemSites = $itemSites | ConvertTo-Json

    $itemBody = @"
{
    "resourcePool": {
        "resourcePermission": {
            "all": false,
            "sites": $('[' + $itemSites.TrimStart('[').TrimEnd(']') + ']')
        }
    }
}
"@

    $put = Invoke-WebRequest -Method Put -Uri ($morphURL + "/api/zones/$($cloud)/$($construct)/$($itemGet.id)") -SkipCertificateCheck -Headers $headers -Body $itemBody -ErrorVariable err
}
}

### DATA STORES

if ($datastores){
    $construct = "data-stores"
    $object = $datastores

    foreach ($item in $object) {
    # Var
    Write-Host "Modifying $($construct): $($item)" -ForegroundColor DarkCyan
    $itemGet = Invoke-WebRequest -Uri ($morphURL + "/api/zones/$($cloud)/$($construct)?name=$($item)") -SkipCertificateCheck -Headers $headers | ConvertFrom-Json | Select-Object -ExpandProperty datastores
    #$itemGet = $itemGet[$itemGet.count -1]
    $itemSites = $itemGet.resourcePermissions.sites
    $itemGroup = New-Object psobject
    $itemGroup | Add-Member NoteProperty -Name id -Value $group
    $itemGroup | Add-Member NoteProperty -Name default -Value True

    $itemSites += $itemGroup
    $itemSites = $itemSites | ConvertTo-Json

    $itemBody = @"
{
    "datastore": {
        "resourcePermission": {
            "all": false,
            "sites": $('[' + $itemSites.TrimStart('[').TrimEnd(']') + ']')
        }
    }
}
"@

    $put = Invoke-WebRequest -Method Put -Uri ($morphURL + "/api/zones/$($cloud)/$($construct)/$($itemGet.id)") -SkipCertificateCheck -Headers $headers -Body $itemBody
}
}

### NETWORKS

if ($networks){
    $construct = "networks"
    $object = $networks

    foreach ($item in $object) {
    # Var
    Write-Host "Modifying $($construct): $($item)" -ForegroundColor DarkCyan
    $itemGet
    $itemGet = Invoke-WebRequest -Uri ($morphURL + "/api/" + $construct + "?name=" + $item) -SkipCertificateCheck -Headers $headers | ConvertFrom-Json | Select-Object -ExpandProperty networks
    #$itemGet = $itemGet[$itemGet.count -1]
    $itemSites = $itemGet.resourcePermissions.sites
    $itemGroup = New-Object psobject
    $itemGroup | Add-Member NoteProperty -Name id -Value $group
    $itemGroup | Add-Member NoteProperty -Name default -Value True

    $itemSites += $itemGroup
    $itemSites = $itemSites | ConvertTo-Json

    $itemBody = @"
{
    "network": {
        "resourcePermission": {
            "all": false,
            "sites": $('[' + $itemSites.TrimStart('[').TrimEnd(']') + ']')
        }
    }
}
"@

# $itemBody = @"
# {
#     "network": {
#         "resourcePermission": {
#             "all": false,
#             "sites": [{
#                 "id: 1,
#                 "default": "true"
#             }]
#         }
#     }
# }
# "@
    $put = Invoke-WebRequest -Method Put -Uri ($morphURL + "/api/$($construct)/$($itemGet.id)") -SkipCertificateCheck -Headers $headers -Body $itemBody
    $put.Content
}
}