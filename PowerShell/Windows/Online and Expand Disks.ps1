<#
    .SYNOPSIS
        This script automatically onlines and expands all drives found by the OS
    
    .DESCRIPTION
        This script automatically onlines and expands all drives found by the OS.
        Note: This does not expand if you have multiple partitions on the same Dynamic root disk as a precaution.
        
        Set this in the Pre-provision and Reconfigure phases of your provisioning Workflow.
        There are additional loops in this to name new drives based on their label in Morpheus. This can be removed easily if not desired.

        Additionally, if you set the code value of your layout to 'sql' it will set properly sized 64k partitions for your additional disks.

    .EXAMPLE
        1. PowerShell task with execute target as 'Resource'
        2. Set Task as Pre-provision and Reconfigure Phase of Provisioning WorkFlow    
#>

# Silence Output
$ProgressPreference = 'SilentlyContinue'

# Remove Recovery Partition (Optional)
Get-Partition | Where-Object -FilterScript {$_.Type -eq 'Recovery'} | Remove-Partition -confirm:$false

#Variables
$disks = get-disk
$size = Get-PartitionSupportedSize -DriveLetter C
$diskorder = '<%= server.volumes.displayOrder.encodeAsJson().toString() %>' | ConvertFrom-Json
$diskname = '<%= server.volumes.name.encodeAsJson().toString() %>' | ConvertFrom-Json
$diskarray = $diskorder | Select-Object @{n='ID'; e={$diskorder[$_]}}, @{n='Name'; e={$diskname[$_]}}
$layout = "<%= instance.layoutCode %>"


foreach ($disk in $disks) {
    #Online, Initialize, Format, and Assign Drive Letter to additional drives
    IF ($disk.IsOffline -eq $true) {
        if ($layout -eq 'sql') {
            Initialize-Disk -Number $disk.DiskNumber -PassThru|
            New-Partition -UseMaximumSize -AssignDriveLetter|
            Format-Volume -NewFileSystemLabel ($diskarray | where {$_.id -eq $disk.number} | select -ExpandProperty name) -FileSystem NTFS -AllocationUnitSize 65536 -confirm:$false
        } else {
            Initialize-Disk -Number $disk.DiskNumber -PassThru|
            New-Partition -UseMaximumSize -AssignDriveLetter|
            Format-Volume -NewFileSystemLabel ($diskarray | where {$_.id -eq $disk.number} | select -ExpandProperty name) -FileSystem NTFS -confirm:$false
        }
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