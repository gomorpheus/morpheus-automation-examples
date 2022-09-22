<#
    .SYNOPSIS
        This script will generate a 7 character "service tag", check it against Active Directory and rename an instance once a unique one has been generated.
        This can be manipulated to modify the submit payload and pre-tasks anyway you see fit.
        It will be typical for the submit to pause while these tasks execute as we are confirming the final payload.
        

    .Notes
        Author: Sean Jabro
        Last Update: 4/26/2022
        This is Morpheus specific PowerShell script as it deals with updating the instance spec.

    .DESCRIPTION
        The steps are as follows:
        1. Generate a 7 Character hostname option to mimic a Dell service tag ID
        2. Check the generated name against Active Directoy to see if the computer name exists in the domain. If it does, repeat steps 1 and 2
        3. Once a unique name has been generated, apply it to the spec config for the hostname of the system.
#>

$ProgressPreference = 'SilentlyContinue'

### VARIABLES

$chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'.ToCharArray()
$newName = ""
$available = $false
$configJson = '<%=spec.encodeAsJson().toString()%>' | ConvertFrom-Json

### SCRIPT

### Generate a 7 char "service tag" and check it against AD until a unique name has been generated
do {
	1..7 | foreach { $newName += $chars | Get-Random}

  try {
      Get-ADComputer $newName
      }catch{
      $available = $true
  }
}
until ($available -eq $true)

### Update the instance name and instance hostname attributes in the configJson object.
$configJson.instance.name = $newName
$configJson.instance.hostname = $newName

### Convert the object to JSON
$configJson = $configJson | ConvertTo-Json -Depth 10

$spec = @"
{
    "spec": $configJson
}
"@

### END SCRIPT ###

### OUTPUT SPEC ### 
$spec
    