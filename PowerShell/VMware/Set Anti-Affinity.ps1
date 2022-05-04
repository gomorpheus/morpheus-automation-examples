<#
.SYNOPSIS
This Script configures a VMware anti-affinity rules for Instances deployed via Morpheus

.DESCRIPTION
Utilizes the Morpheus FE servers as a PowerShell Core/PowerCLI host.  When more than 1 VM is deployed, an anti-affinity rule is created on the cluster to ensure the VMs are seperated.

See notes for additional details on how to configure the task in Morpheus.

.NOTES
1. Create Local PowerShell Task and associate it with a Provisioning Workflow
2. Attach Workflow to Instance Type, or leave user selectable
3. Create a JSON Cypher for each vCenter with the code of the Cloud (This will utilize zone.code Morpheus variable)
4. Install PowerShell core on the Morpheus FE Servers
5. Install PowerCLI (Must be scoped allusers) on the Morpheus FE Servers
6. Launch PowerCLI once and set agree to the PowerCLI terms        
7. Deploy instance. If it has more than a single VM, it will create an anti-affinity rule.

.EXAMPLE
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


.PARAMETER vCenterCreds
Specifies the Cypher secret for vCenter(s) in JSON format

.PARAMETER VMs
Specifices each Hostname of nested VMs

.PARAMETER Instance
Specifies the Instance Name for Rule Creation

#>

$ProgressPreference = "SilentlyContinue"

#Input Variables
$VMs = '<%=instance.containers.server.name%>'
$VMs = $VMs.Replace("[","").Replace("]","").Split(",").TrimStart(" ") | sort-object
$Instance = '<%=instance.name%>'
$vCenterCreds = "<%=cypher.read('secret/' + zone.code)%>"
$ServerName = '<%=server.name%>'

#vCenter Variables
$vCenterCreds = $vCenterCreds | convertfrom-json | select -expandproperty clouds
$vPass = $vCenterCreds.password | ConvertTo-SecureString -asPlainText -Force
$vUser = $vCenterCreds.user
$vCreds = New-Object System.Management.Automation.PSCredential($vUser,$vPass)
$vCenters = $vCenterCreds.url

Write-Host "Execution Server $ServerName" -ForegroundColor White

if ($ServerName -eq $VMs[-1]) {

    $Affinity = @()

    if ($VMs.count -gt 1) {

        #Connect to vCenter(s)
        Write-Host "Connecting to vCenter(s)..." -ForegroundColor Cyan
        foreach($vCenter in $vCenters) {
        connect-viserver $vCenter -Credential $vCreds | out-null
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
        
        Write-Host "Creating Anti-Affinity Group $($AFGCluster + '-' + $Instance)" -ForegroundColor Cyan
        New-DrsRule -Name ($AFGCluster + '-' + $Instance) -VM $Affinity.VM -Server $Server -Cluster $AFGCluster -KeepTogether $false -Enabled $true | out-null
        Write-Host "Completed!" -ForegroundColor Green
    } else {
        Write-Host "Only 1 server in instance!..." -ForegroundColor Cyan
    }
} else {
    Write-Host "Job runs only once!" -ForegroundColor Yellow
}

$LASTEXITCODE