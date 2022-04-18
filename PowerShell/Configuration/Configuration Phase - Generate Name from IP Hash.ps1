<#
    .SYNOPSIS
        Modify Payload of Initial Provision

    .Notes

        This can be manipulated to modify the submit payload and pre-tasks anyway you see fit.
        It will be typical for the submit to pause while these tasks execute as we are confirming the final payload.

    .DESCRIPTION
        The steps are as follows:
        1. Query Morpheus Pool based on Selection, set IP reserved
        2. Pass IP to Name Hashing
        3. Inject Instance Name and Host Name as Hashed Name
        4. Profit

    .PARAMETER bearer
    Specifies a Bearer token for Morpheus Automation

    .PARAMETER morphUrl
    Specifies the Morpheus URL in format 'https://url.com/'

    .PARAMETER configJson
    This is the incoming 'spec' JSON that holds the initial payload.  This is needed to know the pool ID.
    You will always pass the 'spec' variable in which is a system var and not a custom Option Type required.
    
    .EXAMPLE
        1. Local Shell Script Referencing a GIT Repo
        2. Command Example:
            pwsh -file 'path/script.ps1' -morphUrl '<%=morpheus.applianceUrl%>' -bearer "<%=cypher.read('secret/bearer')%>" 
                -configJson '<%=spec.encodeAsJson().toString()%>'
#>

#################################################################################
### Params
Param (
    [Parameter(Mandatory = $true)]$bearer,
    [Parameter(Mandatory = $true)]$morphUrl,
    [Parameter(Mandatory = $true)]$configJson
    #[AllowEmptyString()]$placeholder
)

### Functions
function ipv4ToHexString($ipv4){
 
    # Validation
    $valid = $true
    $ipv4.split(".") | foreach { if([int]$_ -ge 0 -and [int]$_ -le 255) { } else { $valid = $false } }
 
    if($valid -eq $true){
 
        # Conversion
        $hexString = ""
        $hexList = @("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")
        $ipv4.split(".") | foreach {
            $mod = [int]$_ % 16
            $first = $hexList[(([int]$_ - $mod) / 16)]
            $second = $hexList[$mod]
            $hexString += $first+$second
        } 
        return $hexString
    }
    else{
        return $false
    }
}

### Variables
$configJson = $configJson | convertfrom-json -Depth 10
$ContentType = 'application/json'
$morphHeader = @{
    "Authorization" = "BEARER $bearer"
}
$poolApi = 'api/networks/pools/'
$pool = $configJson.networkInterfaces.network.pool.id
$tempName = get-random
$poolBody = @"
{
    "createDns": false,
    "networkPoolIp": {
      "hostname": $tempName
    }
}
"@

#################################################################################
### Script
# Request IP
$ip = (Invoke-WebRequest -Method POST -Uri ($morphUrl + $poolApi + $pool + '/ips') -SkipCertificateCheck -Headers $morphHeader -Body $poolBody -ContentType $ContentType).content | convertfrom-json
$ip = $ip.networkPoolIp

# Generate Name Hash
$hashName = (ipv4ToHexString -ipv4 $ip.ipAddress).toUpper()

# Update JSON

$networkJson = $configJson.networkInterfaces

$configJson.instance.name = $hashName
$configJson.instance.hostName = $hashName
$configJson.customOptions.name = $hashName
$configJson.customOptions.hostName = $hashName
$networkJson | Add-Member NoteProperty -Name ipAddress -Value $ip.ipAddress -f
$networkJson | Add-Member NoteProperty -Name ipMode -Value 'static' -f
$networkJson | Add-Member NoteProperty -Name replaceHostRecord -Value $true -f
$configJson.networkInterfaces = $networkJson

#################################################################################
### Export

$configJson = $configJson | ConvertTo-Json -Depth 10

$spec = @"
{
    "spec": $configJson
}
"@

$spec