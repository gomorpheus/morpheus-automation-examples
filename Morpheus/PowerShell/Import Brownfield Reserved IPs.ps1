<#
    .SYNOPSIS
    Set IP reservations on IP Pools

    .DESCRIPTION
    Take a CSV of Pools, IPs, and Names then compare to IP Pools in Morpheus and set the reservations.
#>

### VARS ###
$File = Read-Host 'File Path EX: C:\temp\migrate.csv'

# Transcript
$outFile = ((Split-Path $File -Resolve) + '\IPImports-' + ([DateTimeOffset]::Now.ToUnixTimeSeconds()) + '.txt')
Start-Transcript -Path $outFile

$Username = Read-Host 'Enter UserName'
$Password = Read-Host 'Enter Password' -AsSecureString
$PlainTextPassword= [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR( ($Password) ))
$URL = '' # Morpheus URL EX: https://myexample.com
$morphURL = $URL.TrimEnd('/')

### Header Variables ###
$Body = "username=$Username&password=$PlainTextPassword"
$authURL = "/oauth/token?grant_type=password&scope=write&client_id=morph-customer"
$morphToken = Invoke-WebRequest -Method POST -Uri ($morphURL + $authURL) -SkipCertificateCheck -Body $Body | select -ExpandProperty content | ConvertFrom-Json | select -ExpandProperty access_token
#$morphToken = ''
$morphHeader = @{
    "Authorization" = "BEARER $morphToken"
    }

### Request Variables ###
$output = @()
$contentType = 'application/json'
$poolURL = '/api/networks/pools/'

#----------------------------------------------------#
### Functions ###
function Get-TimeStamp {    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)    
}

### Script ###
### Inventory Excel Data ###
Write-Host "$(Get-TimeStamp) Gathering Excel Data..." -ForegroundColor Cyan
$IPs = Import-Csv -Path $file

### Inventory Morpheus Pools ###
Write-Host "$(Get-TimeStamp) Gathering Morpheus Pools..." -ForegroundColor Cyan
$morphPools = (Invoke-WebRequest -Method Get -Uri ($morphURL + $poolURL + '?max=10000') -SkipCertificateCheck -Headers $morphHeader).content | ConvertFrom-Json |
select -ExpandProperty networkPools | select id, name


Write-Host "$(Get-TimeStamp) Finished Gathering Phases..." -ForegroundColor Green

Write-Host "$(Get-TimeStamp) Begin Executing Script..." -ForegroundColor Yellow

Write-Host "$(Get-TimeStamp) Tracking IPs..." -ForegroundColor Yellow

foreach ($IP in $IPs) {
    $out = New-Object PSObject
    $pool = $null
    $server = $null
    $address = $null
    $pool = $morphPools | where Name -EQ $IP.Network
    $server = $IP.Name
    $address = $IP.IP

    if (!$server) {
        $server = 'UNKNOWN'
    } else {
        $Body = @"
{
    "networkPoolIp": {
        "ipAddress": $address,
        "hostname": $server
    }
}
"@
    try {
        # Submit IP
        Invoke-WebRequest -Method Post -Uri ($morphURL + $poolURL + $($pool.id) + '/ips') -SkipCertificateCheck -Headers $morphHeader -Body $Body -ContentType $contentType | out-null
    } catch {
        Write-Host "$(Get-TimeStamp) Unable to reserve $IP.  $_" -ForegroundColor Red
        $out | Add-Member NoteProperty Name $server
        $out | Add-Member NoteProperty IP $address
        $out | Add-Member NoteProperty Pool $pool
        $out | Add-Member NoteProperty Issue 'Failed to Reserve IP Address'

        $output += $out 
    }

    }
}

Write-Host `r`n
Write-Host "$(Get-TimeStamp) Finished Ingesting IPs!" -ForegroundColor Green

Write-Host `r`n
Write-Host "A full transcript of this session can be found at $($outFile)" -ForegroundColor Cyan