### Morpheus Environment Variables ###
$morpheusURL = '<%=morpheus.applianceUrl%>'
$bearerToken = '<%=morpheus.apiAccessToken%>'

### Script Variables ###
$headers=@{}
$headers.Add("content-type", "application/json")
$headers.Add("authorization", "Bearer $bearerToken")

### Begin Script ###
Write-Host 'Begin Script...' -ForegroundColor Green

### Functions ###
function add-Input ($name,$fieldName,$description,$type,$id,$required) {
    if($id) {
        $body = @"
{
    "optionType": {
            "type": $type,
            "required": $required,
            "exportMeta": false,
            "editable": false,
            "name": $name,
            "description": "$description",
            "fieldName": $fieldName,
            "fieldLabel": $name,
            "placeholder": "$description",
            "optionList": {
                "id": $id
            }
    }
}
"@
    } else {
        $body = @"
{
    "optionType": {
            "type": $type,
            "required": $required,
            "exportMeta": false,
            "editable": false,
            "name": $name,
            "description": "$description",
            "fieldName": $fieldName,
            "fieldLabel": $name,
            "placeholder": "$description"
    }
}
"@
    }

    Write-Host "Creating $name Input..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri ($morpheusURL + '/api/library/option-types') -Method POST -Headers $headers -ContentType 'application/json' -Body $body
 }