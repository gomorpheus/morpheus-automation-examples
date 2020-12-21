Import-Module ServerManager
Add-windowsfeature GPMC
Add-windowsfeature Backup-Features
Add-windowsfeature Backup
Add-windowsfeature Backup-Tools
Add-windowsfeature Wins-Server
Add-windowsfeature AS-NET-Framework
Add-windowsfeature ADDS-Domain-Controller
Add-windowsfeature AD-Domain-Services 

$DCPromoTXT = "$env:windir\temp\dcpromo.txt"
New-Item $DCPromoTXT -Type file
$Domain = "<%=customOptions.domainName%>" 
$DomainNetbiosName = "<%=customOptions.netbiosName%>"
$Password = "bertram4Admin!"  

            $DCPromoTXTContent = 
@"
[DCInstall]
ReplicaOrNewDomain=Domain
NewDomain=Forest
NewDomainDNSName=$Domain
ForestLevel=4
DomainNetbiosName=$DomainNetbiosName
DomainLevel=4
InstallDNS=Yes
ConfirmGc=Yes
DatabasePath="C:\Windows\NTDS"
LogPath="C:\Windows\NTDS"
SYSVOLPath="C:\Windows\SYSVOL"
SafeModeAdminPassword=$($Password)
RebootOnCompletion=NO
"@

Add-Content -Value $DCPromoTXTContent -Path $DCPromoTXT | Out-Null
cmd /c call dcpromo.exe /unattend:$($DCPromoTXT)  
$dcpromo_ExitCode = $LASTEXITCODE