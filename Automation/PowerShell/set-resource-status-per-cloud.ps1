<#
    .SYNOPSIS
        This script is designed to set the active status of objects in Morpheus in bulk.
    .DESCRIPTION
         Networks, Domains, Datastores, Resource Pools and Folders can be set using this script by flipping the correct switch in the call.
         An array of objects you want to keep untouched can be put in the call as well using comma separated values.
    
        ASSUMPTIONS:

        - You have an API token for an admin account in Morpheus
        - The cloud is already attached to Morpheus
        - You have the ID of the cloud
        - You are running this script from powershell core to allow for the -skipCertificateCheck switch to be used on the Invoke-WebRequest command
    
    Known Issues: The -enable switch is not currently working for resource pools for some reason. Disable works fine. Will investigate when I feel like it. -SJ

    .PARAMETER Morpheus_URL
        This is the URL for the Morpheus Appliance

    .PARAMETER token
        This is the API token for the Morpheus account with access to modify the teh resources

    .PARAMETER Zone_ID
        The ID of the Zone that this script will be run against

    .PARAMETER Object_To_Set
        Enter the name or names of the ojbects types you would like to affect in comma separated list
            -   domain
            -   network
            -   folder
            -   resourcePool
            -   datastore

    .PARAMETER enable
        When this switch is set, the script will enable all objects specified, unless explicitly excluded by the Untouched_* parameters.
        The default action of the script is to disable objects.

    .PARAMETER Untouched_Networks
        This parameter takes an array input and will ignore the provided networks when the script is run. 
        Example: -Untouched_Networks "Net_1","Net_3" 
        In this example, Net_1 and Net_3 will remain untouched in Morpheus

    .PARAMETER Untouched_Domains
        This parameter takes an array input and will ignore the provided domains when the script is run. 
        Example: -Untouched_Domains "localdomain","mysweetassdomain.com" 
        In this example,localdomain and mysweetassdomain.com will remain untouched in Morpheus

    .PARAMETER Untouched_Datastores
        This parameter takes an array input and will ignore the provided data stores when the script is run. 
        Example: -Untouched_Datastores "DS_01","DS_03" 
        In this example, DS_01 and DS_03 will remain untouched in Morpheus

    .PARAMETER Untouched_ResourcePools
        This parameter takes an array input and will ignore the provided resource pools when the script is run. 
        Example: -Untouched_ResourcePools "RP_01","RP_03" 
        In this example, RP_01 and RP_03 will remain untouched in Morpheus

    .PARAMETER Untouched_Folders
        This parameter takes an array input and will ignore the provided folders when the script is run. 
        Example: -Untouched_Folders "Folder_01","Folder_03" 
        In this example, Folder_01 and Folder_03 will remain untouched in Morpheus

    .EXAMPLE
        .\set-resource-status-per-cloud.ps1 -Morpheus_URL "https://morpheus.cloud.com" -token 12345qwert -zoneID 3 -Object_To_Set network,datastore,resourcePool,folder -Untouched_Networks "Net_01","Net_03" -Untouched_Datastores "ds_01","ds_01" -Untouched_ResourcePools "RP_01","RP_03" -Untouched_Folders "Folder_1","Folder_2"

        In this example Networks, Datastores, Resourec Pools and Folders are all disabled with the exception of the ones specified in their given parameters

    .EXAMPLE
        ​.\set-resource-status-per-cloud.ps1 -morphURL "https://morpheus.cloud.com" -token 12345qwert -zoneID 3  -Object_To_Set folder -activeFolders "Folder_1","Folder_2"

        In this example, only folders are disabled excluding Folder_1 and Folder_2

    .EXAMPLE
        ​.\set-resource-status-per-cloud.ps1 -morphURL "https://morpheus.cloud.com" -token 12345qwert -zoneID 3 -Object_To_Set folder,datastore,resourcePool,network,domain -enable

        In this example ALL objects the script can enable are enabled via use of the -enable switch

    .EXAMPLE
        ​.\set-resource-status-per-cloud.ps1 -morphURL "https://morpheus.cloud.com" -token 12345qwert -zoneID 3 -Object_To_Set network -Untouched_Networks net-1,net-2 -enable

        In this example all networks but the ones specified in the -Untouched_Networks parmeter will be enabled.

    .NOTES
        Version: 2.0
        Author: Sean Jabro
        Created: 9/03/2020
        Updated: 9/18/2020
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$Morpheus_URL,
    [Parameter(Mandatory=$true)]
    [ValidateSet("network","domain","datastore","resourcePool","folder")]
    [string[]]$Object_To_Set,
    [Parameter(Mandatory=$true)]
    [string]$Zone_ID,
    [Parameter(Mandatory=$true)]
    [string]$token,
    [Parameter(Mandatory=$false)]
    [string[]]$Untouched_Networks,
    [Parameter(Mandatory=$false)]
    [string[]]$Untouched_Domains,
    [Parameter(Mandatory=$false)]
    [string[]]$Untouched_Datastores=@(),
    [Parameter(Mandatory=$false)]
    [string[]]$Untouched_ResourcePools=@(),
    [Parameter(Mandatory=$false)]
    [string[]]$Untouched_Folders=@(),
    [switch]$enable
)

### Formatting enabled switch since you cant .toLower a switch object for some silly reason
$enabled = $enable.ToString()
$enabled = $enabled.ToLower()

### Creating a timestamp for logging clarity 
filter timestamp {"$(Get-Date -Format G): $_"}

### Building the function to do all the heavy lifting.
function  get-apiEndpoint {
    param (
        [Parameter(Mandatory=$true)]
        [ValidateSet("network","domain","datastore","resourcePool","folder")]
        [string]$object,
        [Parameter(Mandatory=$true)]
        [string]$zoneID
    )
    
    switch ($object){
            "Network"       {$properties = @{
                getEndpoint     = "/api/networks?zone=$zoneID&max=10000"
                putEndpoint     = "/api/networks/"
                getContentName  = "networks"
                putContentName  = "network"
                activeSwitch    = $Untouched_Networks
            }
        }
            "Domain"        {$properties = @{
                getEndpoint     = "/api/networks/domains?max=10000"
                putEndpoint     = "/api/networks/domains/"
                getContentName  = "networkDomains"
                putContentName  = "networkDomain"
                activeSwitch    = $Untouched_Domains
            }
        }
            "Datastore"     {$properties = @{
                getEndpoint     = "/api/zones/$zoneID/datastores?max=10000"
                putEndpoint     = "/api/networks/domains/"
                getContentName  = "datastores"
                putContentName  = "datastore"
                activeSwitch    = $Untouched_Datastores
            }
        }
            "ResourcePool"  {$properties = @{
                getEndpoint     = "/api/zones/$zoneID/resource-pools?max=10000"
                putEndpoint     = "/api/zones/$zoneID/resource-pools/"
                getContentName  = "resourcePools"
                putContentName  = "resourcePool"
                activeSwitch    = $Untouched_ResourcePools
            }
        }
            "Folder"        {$properties = @{
                getEndpoint     = "/api/zones/$zoneID/folders?max=10000"
                putEndpoint     =  "/api/zones/$zoneID/folders/"
                getContentName  = "folders"
                putContentName  = "folder"
                activeSwitch    = $Untouched_Folders
            }
        }
    }

    $result = New-Object psobject -property $properties
    $result
}

# Creating headers for API calls
$headers = @{
    Authorization = "Bearer $token"
}

# Get the endpoint data for each selected object type
foreach ($object in $Object_To_Set){
    $touchedObjects = @()
    $untouchedObjects = (get-apiEndpoint -object $object -zoneID $Zone_ID).activeSwitch

    ### Call function to get endpoint and content names for each selected object to disable
    $endpoint = (get-apiEndpoint -object $object -zoneID $Zone_ID).getEndpoint
    $getContentName = (get-apiEndpoint -object $object -zoneID $Zone_ID).getContentName
    $putContentName = (get-apiEndpoint -object $object -zoneID $Zone_ID).putContentName

    Write-Output "You selected $object. Validating any $object's to leave active..." | timestamp
    Write-Output "$($getContentName) to leave alone: $untouchedObjects" | timestamp
    Write-Output "Gathering data from: $Morpheus_Url$endpoint)" | timestamp

    ### Getting payload from API endpoint
    $get = Invoke-WebRequest -SkipCertificateCheck -Uri "$Morpheus_URL$endpoint" -Headers $headers
    $content = ($get | Select-Object -ExpandProperty content |  ConvertFrom-Json).$getContentName

    Write-Output "API Call status code: $($get.StatusCode) $($get.StatusDescription) Found data name: $getContentName" | timestamp

    ### Parse the payload and put any objects not defined in the -Untouched_* paramter in the the $touchedObjects object
    foreach ($obj in $content){
        if ($obj.name -notin $untouchedObjects){
            $touchedObjects += $obj
        }
    }

    ### Run the PUT API call to set the status of the object
    foreach ($obj in $touchedObjects){
        Write-Output "Attempting to set status of $($obj.name) of type $object..." | timestamp
        $id = $obj.id
        $endpoint = (get-apiEndpoint -object $object -zoneID $Zone_ID).putEndpoint
        $body = @{$putContentName = @{active = "$($enabled)"}} | ConvertTo-Json -Depth 10 | ForEach-Object {[System.Text.RegularExpressions.Regex]::Unescape($_)}
        $URL = $Morpheus_URL+$endpoint+$id
        Write-Output "Setting active status to $($enable) at: $URL" | timestamp
        $output = Invoke-WebRequest -SkipCertificateCheck -Method PUT -Uri $URL -Headers $headers -Body $body
        Write-Output "API call status code return: $($output.StatusCode) $($output.StatusDescription)" | timestamp
    }

}
