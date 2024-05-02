<#
    .SYNOPSIS
        This script automatically deletes AD Objects, IPV4, IPV6, PTR, and any other records that need to be cleaned up EOL.
    
    .DESCRIPTION
        This script automatically deletes AD Objects, IPV4, IPV6, PTR, and any other records that need to be cleaned up EOL.        
        This should be ran in the teardown phase of a provisioning workflow, or manually before deleting a server.
        Run the task against remote, and esnure that the dns powershell module is available on the jumpbox server.

    .EXAMPLE
        1. PowerShell task with execute target as 'Remote', ensure Elevated Shell is checked.
        2. Set Task as Teardown Phase of Provisioning WorkFlow
#>

# Silence Output
$ProgressPreference = 'SilentlyContinue'

klist purge -li 0x3e7  

# Variables
$domain = "<%=instance.domainName%>"
$serverName = "<%= container.server.name %>"
$serverName = $serverName.Split('.')[0]
$reverseZone = " +'.in-addr.arpa'"

# Remove DNS Records
Write-Host "Gathering DNS Records..." -ForegroundColor Cyan
$records = Get-DnsServerResourceRecord -ZoneName $domain -name $serverName
Write-Host "Complete!" -ForegroundColor Green

$IPAddress = ($records | where RecordType -eq 'A').RecordData.IPv4Address.IPAddressToSTring

ForEach ($record in $records) {
	Write-Host "Attempting to remove ${$record.RecordType}..." -ForegroundColor Cyan
	Remove-DnsServerResourceRecord -ZoneName $domain -name $serverName -RRType $record.RecordType -force
    Write-Host "Complete!" -ForegroundColor Green
}
	
# Remove PTR RecordType
$IPAddressArray = $IPAddress.Split(".")
$reverseZone = ($IPAddressArray[2]+"."+$IPAddressArray[1]+"."+$IPAddressArray[0] +'.in-addr.arpa')

try {
	Write-Host "Attempting to remove PTR..." -ForegroundColor Cyan
	Remove-DnsServerResourceRecord -ZoneName $reverseZone -name $IPAddressArray[3] -RRType Ptr -force -ErrorAction SilentlyContinue
    Write-Host "Complete!" -ForegroundColor Green
} catch {$null}

#Remove AD Object (Cleans up A)
try {
	Write-Host "Attempting to remove $severName AD Object..." -ForegroundColor Cyan
	Remove-ADComputer -server $domain -identity $serverName -confirm:$false
    Write-Host "Complete!" -ForegroundColor Green
} catch {$null}