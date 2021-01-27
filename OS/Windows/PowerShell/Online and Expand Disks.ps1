<#
    .SYNOPSIS
        This script automatically onlines and expands all drives found by the OS
    
    .DESCRIPTION
        This script automatically onlines and expands all drives found by the OS.
        Note: This does not expand if you have multiple partitions on the same Dynamic root disk as a precaution.
        
        Set this in the Pre-provision and Reconfigure phases of your provisioning Workflow.
        There are additional loops in this to name new drives based on their label in Morpheus. This can be removed easily if not desired.

    .EXAMPLE
        1. PowerShell task with execute target as 'Resource'
        2. Set Task as Pre-provision and Reconfigure Phase of Provisioning WorkFlow    
#>

#Variables
$disks = get-disk
$size = Get-PartitionSupportedSize -DriveLetter C
$MorphOrder = "<%=server.volumes.displayOrder%>"
$MorphName = "<%=server.volumes.name%>"
$diskorder = $MorphOrder.Replace("[","").Replace("]","").Split(",").TrimStart(" ")
$diskname = $MorphName.Replace("[","").Replace("]","").Split(",").TrimStart(" ")
$diskarray = $diskorder | Select-Object @{n='ID'; e={$diskorder[$_]}}, @{n='Name'; e={$diskname[$_]}}


foreach ($disk in $disks) {
    #Online, Initialize, Format, and Assign Drive Letter to additional drives
    IF ($disk.IsOffline -eq $true) {
        Initialize-Disk -Number $disk.DiskNumber -PassThru|
        New-Partition -UseMaximumSize -AssignDriveLetter|
        Format-Volume -NewFileSystemLabel ($diskarray | where {$_.id -eq $disk.number} | select -ExpandProperty name) -FileSystem NTFS -confirm:$false
    }
    #Confirm disk only has 1 partition with a drive letter, expand to max size.  Skip Multiple Drive Letters
    ELSE {
        $partition = $disk | Get-Partition | where DriveLetter -ne "`0"

        if (($partition | measure).count -eq 1) {
            $maxSize = (Get-PartitionSupportedSize -DriveLetter $partition.DriveLetter).sizeMax
            Resize-Partition -DriveLetter $partition.DriveLetter -Size $maxSize -ErrorAction SilentlyContinue
            }
        
    }
}
    
Exit