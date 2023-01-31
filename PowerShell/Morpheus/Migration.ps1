<#
    .SYNOPSIS
        Migration script that moves managed instances

    .DESCRIPTION
        This will convert systems to managed in Morpheus and set ownership.
        
        NOTE: This does not support installing Agent yet...
#>

### Original Server Inventory ###
#$File = '<FILE PATH>'  # Path to CSV file.  Expected headers 'Name' (Server Name), 'Email' (Owner Email Address), 'Group' (Owner Morpheus Group Name)
$File = Read-Host 'File Path EX: C:\temp\migrate.csv'

# Transcript
$outFile = ((Split-Path $File -Resolve) + '\MigrationRun-' + ([DateTimeOffset]::Now.ToUnixTimeSeconds()) + '.txt')
Start-Transcript -Path $outFile

### Morpheus Variables ###
#$morphToken = '<API TOKEN>' # Create and Enter Admin Morpheus Token
#$morphURL = "https://<URL>" # Enter Morpheus URL
$Username = Read-Host 'Enter UserName'
$Password = Read-Host 'Enter Password' -AsSecureString
$PlainTextPassword= [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR( ($Password) ))
$URL = Read-Host 'Morpheus URL EX: https://myexample.com'
$morphURL = $URL.TrimEnd('/')

### Header Variables ###
$Body = ('username=$Username&password=' + $PlainTextPassword)
$authURL = "/oauth/token?grant_type=password&scope=write&client_id=morph-customer"
$morphToken = Invoke-WebRequest -Method POST -Uri ($morphURL + $authURL) -Body $Body | select -ExpandProperty content | ConvertFrom-Json | select -ExpandProperty access_token
$morphHeader = @{
    "Authorization" = "BEARER $morphToken"
    }

### Request Variables ###
$output = @()
$instanceURL = '/api/instances/'
$serverURL = '/api/servers/'
$userURL = '/api/users/'
$groupURL = '/api/groups/'
$ContentType = 'application/json'
#-----------------------------------------------------------------------------------------#



### Functions ###
function Get-TimeStamp {    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)    
}

### Inventory Excel Data ###
Write-Host "$(Get-TimeStamp) Gathering Excel Data..." -ForegroundColor Cyan
$Instances = Import-Csv -Path $file

### Inventory Morpheus Users ###
Write-Host "$(Get-TimeStamp) Gathering Morpheus Users..." -ForegroundColor Cyan
$morphUsers = (Invoke-WebRequest -Method Get -Uri ($morphURL + $userURL + '?max=10000') -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty users | select id, username, email

### Inventory Morpheus Groups ###
Write-Host "$(Get-TimeStamp) Gathering Morpheus Groups..." -ForegroundColor Cyan
$morphGroups = (Invoke-WebRequest -Method Get -Uri ($morphURL + $groupURL + '?max=10000') -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty groups | select id, name

### Inventory Morpheus Servers ###
Write-Host "$(Get-TimeStamp) Gathering Morpheus Known Servers..." -ForegroundColor Cyan
$newServers = (Invoke-WebRequest -Method Get -Uri ($morphURL + $serverURL + '?max=10000') -Headers $morphHeader).content | ConvertFrom-Json | select -ExpandProperty servers | select id, name, @{n='code';e={($_.computeServerType).code}}
$newServers = $newServers | where code -like "*Unmanaged*"

Write-Host "$(Get-TimeStamp) Finished Gathering Phases..." -ForegroundColor Green

### Run Convert to Managed Script ###
Write-Host "$(Get-TimeStamp) Begin Executing Management Script..." -ForegroundColor Yellow

Write-Host "$(Get-TimeStamp) Managing Instances..." -ForegroundColor Yellow

foreach ($Instance in $Instances) {
    $out = New-Object PSObject
    $err = 0
    $user = $null
    $group = $null
    $managedId = $null
    $Server = $null
    $Server = $newServers | where Name -EQ $Instance.Name
    $group = $morphGroups | where Name -EQ $Instance.Group
    $user = $morphUsers | where Email -EQ $Instance.Email

    if (!$user) {
        Write-Host "$(Get-TimeStamp) User $($User.email) Not Found for Server $($Instance.Name)" -ForegroundColor Yellow
        $out | Add-Member NoteProperty Name $Instance.Name
        $out | Add-Member NoteProperty Email $Instance.Email
        $out | Add-Member NoteProperty Issue 'User Not Found'

        $output += $out 
    } Else {
    $Body = @"
{
    "server": {
    "sshPassword": "",
    "sshUsername": "root",
    "provisionSiteId": $($group.Id)
    },
    "installAgent": false
}
"@

    $ownerBody = @"
{
    "instance": {
    "ownerId": $($user.Id)
    }
}
"@

        if (!$server) {
            Write-Host "$(Get-TimeStamp) Server $($Instance.Name) Not Found!" -ForegroundColor Red
            $out | Add-Member NoteProperty Name $Instance.Name
            $out | Add-Member NoteProperty Email $Instance.Email
            $out | Add-Member NoteProperty Issue 'Server Not Found'
    
            $output += $out 
        }
        else {
            Write-Host "$(Get-TimeStamp) Putting server $($Instance.Name) under management..." -ForegroundColor Gray

            try {
                Invoke-WebRequest -Method Put -Uri ($morphURL + $serverURL + $Server.id + '/install-agent') -Headers $morphHeader -Body $Body -ContentType $ContentType -ErrorAction Inquire | Out-Null
                Start-Sleep 2
            }
            catch {
                $err = 1
                Write-Host "$(Get-TimeStamp) Unable to manage server $($Instance.Name).  $_" -ForegroundColor Red
                $out | Add-Member NoteProperty Name $Instance.Name
                $out | Add-Member NoteProperty Email $Instance.Email
                $out | Add-Member NoteProperty Issue 'Failed to Manage Server'
        
                $output += $out 
            }

            if ($err -eq 0) {
                try {
                    # Grab Instance Id
                    $managedId = Invoke-WebRequest -Method Get -Uri ($morphURL + $instanceURL + '?name=' + $Instance.Name) -Headers $morphHeader | ConvertFrom-Json | select -ExpandProperty instances | select -ExpandProperty id
                    
                    # Set Owner
                    Write-Host "--Setting Owner $($User.email) on server $($Instance.Name)..." -ForegroundColor Gray
                    Invoke-WebRequest -Method Put -Uri ($morphURL + $instanceURL + $managedId) -Headers $morphHeader -Body $ownerBody -ContentType $ContentType -ErrorAction Inquire | Out-Null
                }
                catch {
                    Write-Host "$(Get-TimeStamp) Unable to set owner on $($Instance.Name).  $_" -ForegroundColor Red
                    $out | Add-Member NoteProperty Name $Instance.Name
                    $out | Add-Member NoteProperty Email $Instance.Email
                    $out | Add-Member NoteProperty Issue 'Failed to Set Owner on Managed Instance'
            
                    $output += $out 
                }
            }
        }
    }
}

Write-Host `r`n
Write-Host "$(Get-TimeStamp) Finished Migration!" -ForegroundColor Green

Write-Host `r`n
Write-Host "$(Get-TimeStamp) The Following Errors Occurred ..." -ForegroundColor Red
Write-Host "A full transcript of this session can be found at $($outFile)" -ForegroundColor Red
Write-Host `r`n

# output Errors
$output