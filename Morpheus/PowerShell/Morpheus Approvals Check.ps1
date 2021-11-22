#!/usr/bin/env pwsh
pwsh -c - <<'EOF'
 
<#
    .SYNOPSIS
        This Script checks for pending approvals in Morpheus - it has been adapted to work for applications
        awaiting approval as well as instances.
    
    .DESCRIPTION
        Configure this script to run as a 'Job' in Morphues.  This can run at your prefered schedule and 
        find any pending approvals and email.
#>
 
$ProgressPreference = "SilentlyContinue"
 
### Variables ###
$Date = Get-Date # Grab current time
$HasApprovals = 0
$morphURL = '<%=morpheus.applianceUrl%>'
$checkTime = '<%=customOptions.checkTime%>'

## serviceBearer needs to be adjusted to use the correct secret from Cypher
$serviceBearer = "<%=cypher.read('secret/Bearer')%>"
 
### Request Variables ###
$Header = @{
    "Authorization" = "BEARER $serviceBearer"
    }
$ContentType = 'application/json'

### Script ###
$Approvals = (Invoke-WebRequest -NoProxy -SkipCertificateCheck -Method Get -Uri ($MorphURL + 'api/approvals?max=1000000') -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty approvals
 
Write-Host "<b>New Approvals Pending Within Last $checkTime Minutes...<br />"
Write-Host "<b>Morpheus Approvals Site: </b><a>$($MorphURL + 'operations/approvals/')</a><br />"
 
foreach ($Approval in $Approvals) {
    if ($Approval.status -like "*requested*") {
        [datetime]$approvalDate = ($Approval.datecreated)

        if ($approvalDate.AddMinutes($checkTime) -ge $Date) {            
            ### Approval Vars ###
            $HasApprovals = 1
            $approvalInfo = (Invoke-WebRequest -NoProxy -SkipCertificateCheck -Method Get -Uri ($MorphURL + 'api/approvals/' + $($Approval.id)) -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty approval
            
            ### Output Data Collected ###
            Write-Host "--------------------------------------------------------------------------------<br />" -ForegroundColor White
            write-host "Pending Morpheus Request: $($approvalInfo.name)<br />" -ForegroundColor Cyan
            write-host "Request Creation Date: $($approvalDate)<br />" -ForegroundColor Cyan
            Write-Host "Requested By: $($approvalInfo.requestBy)<br />" -ForegroundColor Cyan    

            ## Approval could relate to instance or app
            if ($approvalInfo.approvalItems.reference.type -eq "app") {
                $app = (Invoke-WebRequest -NoProxy -SkipCertificateCheck -Method Get -Uri ($MorphURL + 'api/apps/' + $($approvalInfo.approvalItems.reference.id)) -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty app         
                
                ## App specific markup
                Write-Host "Specs:<br /> `
                <p style="margin-left:2.5em">App Name: $($app.name),</p> `
                <p style="margin-left:2.5em">Description: $($app.description),</p> `
                <p style="margin-left:2.5em">Blueprint: $($app.blueprint.name),</p> `
                <p style="margin-left:2.5em">Instances: $($app.stats.instanceCount),</p> `
                <p style="margin-left:2.5em">Max Memory: $($app.stats.maxMemory /1024/1024/1024) GB,</p> `
                <p style="margin-left:2.5em">Max Storage: $($app.stats.maxStorage /1024/1024/1024) GB</p> `
                <br /> `
                " -ForegroundColor Cyan

            } elseif ($approvalInfo.approvalItems.reference.type -eq "instance") {
                $instance = (Invoke-WebRequest -NoProxy -SkipCertificateCheck -Method Get -Uri ($MorphURL + 'api/instances/' + $($approvalInfo.approvalItems.reference.id)) -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty instance                   
                
                ## Instance specific markup
                Write-Host "Specs:<br /> `
                <p style="margin-left:2.5em">Name: $($instance.hostname),</p> `
                <p style="margin-left:2.5em">Plan: $($instance.plan.name),</p> `
                <p style="margin-left:2.5em">Storage: $($instance.maxStorage /1024/1024/1024) GB</p> `
                <br /> `
                " -ForegroundColor Cyan
            }
            
        
            ### Create Approve/Deny Buttons ###
            # Note: Added 'if' to make the buttons nicer for Outlook folks
            Write-Host "
            <div> `
            <!--[if mso]> `
            <v:roundrect xmlns:v='urn:schemas-microsoft-com:vml' xmlns:w='urn:schemas-microsoft-com:office:word' href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/approve')`' style='height:40px;v-text-anchor:middle;width:300px;' arcsize='10%' stroke='f' fillcolor='#00cc00'> `
                <w:anchorlock/> `
                <center style='color:rgb(0, 0, 0);font-family:sans-serif;font-size:16px;font-weight:bold;'> `
                Approve Request `
                </center> `
            </v:roundrect> `
            <![endif]--> `
            <![if !mso]> `
            <table cellspacing='0' cellpadding='0'> `
            <tr> `
            <td align='center' bgcolor='#00cc00' style='-webkit-border-radius: 1px; -moz-border-radius: 1px; border-radius: 1px; color: rgb(0, 0, 0); display: block;'> `
            <a href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/approve')`' style='font-size:16px; font-weight: bold; font-family: Helvetica, Arial, sans-serif; text-decoration: none; line-height:10px; width:20px; display:inline-block'><span style='color: rgba(255, 255, 255, 0.00);Approve</span></a> `
            </td> `
            </tr> `
            </table> `
            <br /> `
            <br /> `
            <![endif]> `
            </div> `
            <br /> `
            "

            Write-Host "
            <div> `
            <!--[if mso]> `
            <v:roundrect xmlns:v='urn:schemas-microsoft-com:vml' xmlns:w='urn:schemas-microsoft-com:office:word' href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/deny')`' style='height:40px;v-text-anchor:middle;width:300px;' arcsize='10%' stroke='f' fillcolor='#cc0000'> `
                <w:anchorlock/> `
                <center style='color:rgb(0, 0, 0);font-family:sans-serif;font-size:16px;font-weight:bold;'> `
                Deny Request `
                </center> `
            </v:roundrect> `
            <![endif]--> `
            <![if !mso]> `
            <table cellspacing='0' cellpadding='0'> `
            <tr> `
            <td align='center' bgcolor='#cc0000' style='-webkit-border-radius: 1px; -moz-border-radius: 1px; border-radius: 1px; color: rgb(0, 0, 0); display: block;'> `
            <a href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/deny')`' style='font-size:16px; font-weight: bold; font-family: Helvetica, Arial, sans-serif; text-decoration: none; line-height:10px; width:20px; display:inline-block'><span style='color: rgba(255, 255, 255, 0.00);Deny</span></a> `
            </td> `
            </tr> `
            </table> `
            <br /> `
            <br /> `
            <![endif]> `
            </div> `
            "

        }
    }
}
if ($HasApprovals -eq 0) {
    write-host "No NEW Approvals Pending..."
    write-host "Exiting"
    exit 1
}
 
EOF