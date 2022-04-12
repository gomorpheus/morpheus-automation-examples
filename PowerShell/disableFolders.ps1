<#
    .SYNOPSIS
        This will bulk enable and disable X in Morpheus.

    .DESCRIPTION
        This will bulk enable and disable X in Morpheus.
#>

#-----------------------------------------------------------------------------------------#

### Variables
$bearer = '' #API Bearer Token with access to make changes
$morphUrl = 'https://example.fqdn.com/' #FQDN with trailing '/'
$cloud = '' #Cloud ID that contains the folders
$foldersApi = "api/zones/$cloud/folders/"
$morphHeader = @{
    "Authorization" = "BEARER $bearer"
    }

#-----------------------------------------------------------------------------------------#
### Enabled Objects
# $enabled = ('folder1','folder6','folder 10')
$enabled = ('Home','VDI','Work')
#-----------------------------------------------------------------------------------------#

### Functions ###
function Get-TimeStamp {    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
}    

# Get Folders
$folders = (Invoke-WebRequest -Method Get -Uri ($morphUrl + $foldersApi + '?max=-1') -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty folders

# Disable Folders
foreach ($folder in $folders) {
    if ($enable -notcontains $folder.name) {
        # Disable Folder
        Write-Host "Disabling $($folder.name)..."
        Invoke-WebRequest -Method Put -Uri ($morphUrl + $foldersApi + $folder.id) -Body '{"folder":{"active": false}}' -Headers $morphHeader
    }
}

# Activate Folders
foreach ($enable in $enabled) {
    $folder = $folders | where name -eq $enable
    # Activate
    Write-Host "Activating $($folder.name)..."
    Invoke-WebRequest -Method Put -Uri ($morphUrl + $foldersApi + $folder.id) -Body '{"folder":{"active": true}}' -Headers $morphHeader
}