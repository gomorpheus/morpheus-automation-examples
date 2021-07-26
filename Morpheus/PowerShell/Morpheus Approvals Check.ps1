#!/usr/bin/env pwsh
pwsh -c - <<'EOF'

<#
    .SYNOPSIS
        This Script checks for pending approvals in Morpheus
    
    .DESCRIPTION
        Configure this script to run as a 'Job' in Morphues.  This can run at your prefered schedule and find any pending approvals and email.
        Assumption of this script, is this will be pulled from a git repo.  If you need to insert this script locally, modify the parameters
        to be actual variables configured from your Morphues.

#>

$ProgressPreference = "SilentlyContinue"

### Variables ###
$Date = Get-Date # Grab current time
$Counter = 0
$serviceBearer = "<%=cypher.read('secret/Bearer')%>"
$morphURL = '<%=morpheus.applianceUrl%>'
$checkTime = '<%=customOptions.checkTime%>'

### Request Variables ###
$Header = @{
    "Authorization" = "BEARER $serviceBearer"
    }
$ContentType = 'application/json'

### Script ###
$Approvals = (Invoke-WebRequest -Method Get -Uri ($MorphURL + 'api/approvals?max=1000000') -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty approvals

Write-Host "New Approvals Pending Within Last $checkTime Minutes...<br />"
Write-Host "<b>Morpheus Approvals Site: </b><a>$($MorphURL + 'operations/approvals/')</a><br />"

if (!($approvals.status -like "*requested*")) {
    write-host 'No Approvals Pending...'
    exit 0
}
else {
    foreach ($Approval in $Approvals) {
        if ($Approval.status -like "*requested*") {
            [datetime]$approvalDate = ($Approval.datecreated)

            if ($approvalDate.AddMinutes($checkTime) -ge $Date) {            
                ### Approval Vars ###
                $Counter = 1
                $Approval = (Invoke-WebRequest -Method Get -Uri ($MorphURL + 'api/approvals/' + $($Approval.id)) -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty approval
                $Instance = (Invoke-WebRequest -Method Get -Uri ($MorphURL + 'api/instances/' + $($approval.approvalItems.reference.id)) -Headers $Header).content | ConvertFrom-Json | select -ExpandProperty instance

                ### Output Data Collected ###
                Write-Host "--------------------------------------------------------------------------------<br />" -ForegroundColor White
                write-host "Pending Morpheus Request: $($approval.name)<br />" -ForegroundColor Cyan
                write-host "Request Creation Date: $($approvalDate)<br />" -ForegroundColor Cyan
                Write-Host "Requested By: $($approval.requestBy)<br />" -ForegroundColor Cyan
                Write-Host "Specs:<br /> `
                <p style="margin-left:2.5em">Name: $($Instance.hostname),</p> `
                <p style="margin-left:2.5em">Plan: $($Instance.plan.name),</p> `
                <p style="margin-left:2.5em">Storage: $($Instance.maxStorage /1024/1024/1024) GB</p> `
                <br /> `
                " -ForegroundColor Cyan
                
                ### Create Approve/Deny Buttons ###
                # Note: Added 'if' to make the buttons nicer for Outlook folks
                Write-Host "
                <div> `
                <!--[if mso]> `
                <v:roundrect xmlns:v='urn:schemas-microsoft-com:vml' xmlns:w='urn:schemas-microsoft-com:office:word' href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/approve')`' style='height:40px;v-text-anchor:middle;width:300px;' arcsize='10%' stroke='f' fillcolor='#00cc00'> `
                    <w:anchorlock/> `
                    <center style='color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;'> `
                    Approve Request `
                    </center> `
                </v:roundrect> `
                <![endif]--> `
                <![if !mso]> `
                <table cellspacing='0' cellpadding='0'> `
                <tr> `
                <td align='center' bgcolor='#00cc00' style='-webkit-border-radius: 1px; -moz-border-radius: 1px; border-radius: 1px; color: #ffffff; display: block;'> `
                <a href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/approve')`' style='font-size:16px; font-weight: bold; font-family: Helvetica, Arial, sans-serif; text-decoration: none; line-height:10px; width:20px; display:inline-block'><span style='color: #FFFFFF'>Approve</span></a> `
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
                    <center style='color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;'> `
                    Deny Request `
                    </center> `
                </v:roundrect> `
                <![endif]--> `
                <![if !mso]> `
                <table cellspacing='0' cellpadding='0'> `
                <tr> `
                <td align='center' bgcolor='#cc0000' style='-webkit-border-radius: 1px; -moz-border-radius: 1px; border-radius: 1px; color: #ffffff; display: block;'> `
                <a href=`'$($MorphURL + 'operations/approvals/' + $($Approval.id) + '/approvalItems/' + $($Approval.id) + '/deny')`' style='font-size:16px; font-weight: bold; font-family: Helvetica, Arial, sans-serif; text-decoration: none; line-height:10px; width:20px; display:inline-block'><span style='color: #FFFFFF'>Deny</span></a> `
                </td> `
                </tr> `
                </table> `
                <br /> `
                <br /> `
                <![endif]> `
                </div> `
                "

                ### Send Email to Approvers ###
                #Send-MailMessage  # Note: Use this if not using a Morpheus Email Task Type
            }
        }
    }
    if ($counter -eq 0) {
        write-host 'No NEW Approvals Pending...'
        exit 0
    }
}

EOF