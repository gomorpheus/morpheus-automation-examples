#! /usr/bin/pwsh

<#
    .SYNOPSIS
        This Script configures a VMware anti-affinity rules for Instances deployed via Morpheus
    
    .DESCRIPTION
        Steps to initiate Anti-Affinity Creation
        1. Create PowerShell Task and associate it with a Provisioning Workflow
        2. Attach Workflow to Instance Type, or leave user selectable
        3. Create a JSON Cypher for each vCenter with the code of the Cloud (This will utilize zone.code)
        4. Install PowerShell core on the Morpheus FE Servers
        5. Install PowerCLI (Must be scoped allusers) on the Morpheus FE Servers
        6. Launch PowerCLI once and set agree to the PowerCLI terms        
        7. Deploy instance. If it has more than a single VM, it will create an anti-affinity rule.
    
    .EXAMPLE
        1. Local Shell Script Referencing a GIT Repo
        2. Command Example:
            pwsh -file 'path/file.ps1' -morphURL '<%=morpheus.applianceUrl%>' -serviceBearer "<%=cypher.read('secret/Bearer')%>"
            -vCenterCreds "<%=cypher.read('secret/' + zone.code)%>" -VMs "<%=instance.containers.hostname%>" -Instance "<%=instance.name%>"
        3. Cred Payload:
            {
            'clouds': [
                    {
                    'url':'ipaddress',
                    'user':'username',
                    'password':'mypassword'
                    }
                ]
            }

    .ExitCodes
        0 - Job Completed Successfully
#>

### Params ###
Param (
    [Parameter(Mandatory = $true)]$serviceBearer,
    [Parameter(Mandatory = $true)]$morphURL,
    [Parameter(Mandatory = $true)]$VMs,
    [Parameter(Mandatory = $true)]$Instance,
    [Parameter(Mandatory = $true)]$vCenterCreds
)

$ProgressPreference = "SilentlyContinue"

#vCenter Variables
$vCenterCreds = $vCenterCreds | convertfrom-json | select -expandproperty clouds
$vPass = $vCenterCreds.password | ConvertTo-SecureString -asPlainText -Force
$vUser = $vCenterCreds.user
$vCreds = New-Object System.Management.Automation.PSCredential($vUser,$vPass)
$vCenters = $vCenterCreds.url

#Morpheus Variables
$VMs = $VMs.Replace("[","").Replace("]","").Split(",").TrimStart(" ")
$Affinity = @()

if ($VMs.count -gt 1) {

    #Connect to vCenter(s)
    foreach($vCenter in $vCenters) {
    connect-viserver $vCenter -Credential $vCreds
    }

    #Create vCenter Property
    New-VIProperty -Name vCenter -ObjectType VirtualMachine -Value {$Args[0].uid.split(":")[0].split("@")[1]}

    foreach ($VM in $VMs) {
        #Variables
        $vmwareVM = Get-VM $VM
        $Cluster = Get-Cluster -VM $vmwareVM | Select -ExpandProperty Name
        $obj = New-Object psobject

        #Add Property to Array
        $obj | Add-Member -MemberType NoteProperty -Name VM -Value $vmwareVM -Force
        $obj | Add-Member -MemberType NoteProperty -Name Cluster -Value $Cluster -Force
        $Affinity += $obj
    }

    #Creation of Affinity Group
    $AFGCluster = $Affinity.Cluster[0]
    $Server = $Affinity.VM.vCenter[0]
    New-DrsRule -Name ($AFGCluster + '-' + $Instance) -VM $Affinity.VM -Server $Server -Cluster $AFGCluster -KeepTogether $false -Enabled $true
}

$LASTEXITCODE