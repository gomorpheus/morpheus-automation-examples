<#
    .SYNOPSIS
        This Script configures a VMware anti-affinity rules for Instances deployed via Morpheus
    
    .DESCRIPTION
        Simple connect to vCenter(s) block that is reusable in PowerShell/Bash+PWSH Tasks

    .EXAMPLE
        1. Local Shell Script Referencing a GIT Repo
        2. Command Example:
            pwsh -file 'path/file.ps1' -vCenterCreds "<%=cypher.read('secret/' + zone.code)%>"
    
    .PARAMETER vCenterCreds
            The JSON block containing connection information for your vCenter(s)
            Cred Payload:
            {
            'clouds': [
                    {
                    'url':'ipaddress',
                    'user':'username',
                    'password':'mypassword'
                    }
                ]
            }
#>

### Params ###
Param (
    [Parameter(Mandatory = $true)]$vCenterCreds
)

#vCenter Variables
$vCenterCreds = $vCenterCreds | convertfrom-json | select -expandproperty clouds
$vPass = $vCenterCreds.password | ConvertTo-SecureString -asPlainText -Force
$vUser = $vCenterCreds.user
$vCreds = New-Object System.Management.Automation.PSCredential($vUser,$vPass)
$vCenters = $vCenterCreds.url

#Connect to vCenter(s)
foreach($vCenter in $vCenters) {
    connect-viserver $vCenter -Credential $vCreds
}