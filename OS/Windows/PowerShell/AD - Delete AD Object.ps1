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

$domain = "<%=container.domainName%>"
$serverName = "<%= container.server.name %>"
$serverName = $serverName.Split('.')[0]
$reverseZone = " +'.in-addr.arpa'"

#Remove AD Object (Cleans up A)
Remove-ADComputer -identity $serverName -confirm:$false

#Remove PTR
Remove-DnsServerResourceRecord -ZoneName $domain -Name $serverName -RRType PTR -ErrorAction SilentlyContinue

#Remove other DNS Records
$records = Get-DnsServerResourceRecord -ZoneName $domain -Name $serverName
foreach ($record in $records) {
    
    $IPAddress = $record.RecordData.IPv4Address.IPAddressToString
    $IPAddressArray = $IPAddress.Split(".")
    $IPAddressFormatted = $IPAddressArray[3]
    $reverseZone = ($IPAddressArray[2]+"."+$IPAddressArray[1]+"."+$IPAddressArray[0] +'.in-addr.arpa')
    
    #Remove A and AAAA
    Remove-DnsServerResourceRecord -ZoneName $domain -Name $serverName -ErrorAction SilentlyContinue
    
    #Remove PTR
    Remove-DnsServerResourceRecord -ZoneName $domain -Name $serverName
    }