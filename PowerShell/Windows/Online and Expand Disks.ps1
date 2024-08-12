<#
    .SYNOPSIS
        This script automatically onlines and expands all drives found by the OS.
    
    .DESCRIPTION
        This script automatically onlines and expands all drives found by the OS.
        Note: This does not expand if you have multiple partitions on the same Dynamic root disk as a precaution.
        
        Add Task to the (Pre/Post)Provisioning and Reconfigure phases of your Windows Provisioning Workflow.

        There are additional loops in this to name new drives based on their label in Morpheus. This can be removed easily if not desired.

        Additionally, if you set the code value of your layout to 'sql' it will set properly sized 64k partitions for your additional disks.

    .EXAMPLE
        1. PowerShell task with execute target as 'Resource'.
        2. Add Task to the (Pre/Post)Provisioning and Reconfigure Phases of the Windows Provisioning WorkFlow.
#>

# Silence Output
$ProgressPreference = 'SilentlyContinue'

# Change DVD Drive to Z:
# Get the associated volume
$volume = get-volume | Where-Object {$_.DriveType -eq 'CD-ROM' -or $_DriveType -eq 'DVD'}

# Check if the current drive letter is not already Z
# Create a script for diskpart
if ($dvdDrive.DriveLetter -ne 'Z') {
    # Create the diskpart commands as a string
    $diskpartCommands = @"
select volume $($volume.DriveLetter)
assign letter=Z
"@

# Create a temporary file
$tempFile = New-TemporaryFile
$diskpartCommands | Set-Content -Path $tempFile.FullName

# Run diskpart with the temporary file
Start-Process diskpart -ArgumentList "/s $($tempFile.FullName)" -NoNewWindow -Wait
}

# Remove Recovery Partition (Optional)
Write-Host "Checking Recovery Partition Status..." -ForegroundColor Cyan
Get-Partition | Where-Object -FilterScript {$_.Type -eq 'Recovery'} | Remove-Partition -confirm:$false
Write-Host "Complete!" -ForegroundColor Green

# Variables
$disks = Get-Disk
$allDisks = '<%= server.volumes.encodeAsJson() %>' | ConvertFrom-Json
$tempVolume = Get-Volume -FriendlyName 'Temporary Storage' -ErrorAction SilentlyContinue
$layout = "<%= instance?.layoutCode %>"

# Azure decided to have temporary disks and need to account for that
if ($tempVolume) {
    Write-Host "Temporary Disk Identified"
    foreach ($disk in $allDisks) {
        if ($disk.displayOrder -ne 0) {
            $disk.displayOrder++
        }
    }
}

foreach ($disk in $disks) {
    $label = $allDisks | where {$_.displayOrder -eq $disk.number} | select -ExpandProperty name
    if (!($label)) {
        continue # disk not found, skip
    }
    Write-Host "Checking Disk `"${label}`"..." -ForegroundColor Cyan

    # Online, Initialize, Format, and Assign Drive Letter to additional drives
    try {    
        if (($disk.IsOffline -eq $true) -or ($disk | Where-Object PartitionStyle -eq 'RAW')) {
            if ($layout -eq 'sql') {
                Write-Host "Initializing SQL Disk `"${label}`"..." -ForegroundColor White
                Initialize-Disk -Number $disk.number -PassThru|
                New-Partition -UseMaximumSize -AssignDriveLetter|
                Format-Volume -NewFileSystemLabel $label -FileSystem NTFS -AllocationUnitSize 65536 -confirm:$false | Out-Null
            } else {
                Write-Host "Initializing Disk `"${label}`"..." -ForegroundColor White
                Initialize-Disk -Number $disk.number -PassThru|
                New-Partition -UseMaximumSize -AssignDriveLetter|
                Format-Volume -NewFileSystemLabel $label -FileSystem NTFS -confirm:$false | Out-Null
            }
        } else {
            # Confirm disk only has 1 partition with a drive letter, expand to max size, otherwise skip.
            $partition = $disk | Get-Partition | where DriveLetter -ne "`0"
    
            if (($partition | measure).count -eq 1) {
                $maxSize = ($partition | Get-PartitionSupportedSize).sizeMax
                $ms = [math]::round($maxSize/1GB, 2)
                if (($maxSize - $partition.Size) -ge 1000000) {
                    Write-Host "Resizing Disk `"${label}`" to ${ms}GB..." -ForegroundColor White
                    Resize-Partition -DriveLetter $partition.DriveLetter -Size $maxSize -ErrorAction SilentlyContinue
                } else {
                    Write-Host "No Resize Required!" -ForegroundColor Green
                }
            }
        }
    } catch {
        Write-Host "An Error Occurred for Disk `"${label}`":" -ForegroundColor Red
        Write-Host $_
    } finally {
        Write-Host "Disk `"${label}`" Complete!" -ForegroundColor Green
    }
}
    
Exit