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