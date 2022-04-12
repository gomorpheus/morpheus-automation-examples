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

klist purge -li 0x3e7  

# Variables
$domain = "<%=instance.domainName%>"
$serverName = "<%= container.server.name %>"
$serverName = $serverName.Split('.')[0]
$reverseZone = " +'.in-addr.arpa'"

# Remove DNS Records
$records = Get-DnsServerResourceRecord -ZoneName $domain -name $serverName
$IPAddress = ($records | where RecordType -eq 'A').RecordData.IPv4Address.IPAddressToSTring

ForEach ($record in $records) {
	Write-Host "Attempting to remove ${$record.RecordType}..."
	Remove-DnsServerResourceRecord -ZoneName $domain -name $serverName -RRType $record.RecordType -force
}
	
# Remove PTR RecordType
$IPAddressArray = $IPAddress.Split(".")
$IPAddressFormatted = $IPAddressArray[3]
$reverseZone = ($IPAddressArray[2]+"."+$IPAddressArray[1]+"."+$IPAddressArray[0] +'.in-addr.arpa')

try {
	Write-Host "Attempting to remove PTR..."
	Remove-DnsServerResourceRecord -ZoneName $reverseZone -name $IPAddressArray[3] -RRType Ptr -force -ErrorAction SilentlyContinue
} catch {$null}

#Remove AD Object (Cleans up A)
try {
	Write-Host "Attempting to remove $severName AD Object..."
	Remove-ADComputer -server $domain -identity $serverName -confirm:$false
} catch {$null}