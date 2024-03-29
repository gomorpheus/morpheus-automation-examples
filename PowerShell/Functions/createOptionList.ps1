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
function add-OptionList ($name,$fieldName,$description,$json,$required) {
    $json = $json | ConvertTo-Json -Compress
    $name = $name
    $body = @"
{
    "optionTypeList": {
         "type": "manual",
         "visibility": "public",
         "name": $name,
         "initialDataset": $json
    }
}
"@
    Write-Host "Creating $name Option List..." -ForegroundColor White
    Invoke-WebRequest -Uri ($morpheusURL + 'api/library/option-type-lists') -Method POST -Headers $headers -ContentType 'application/json' -Body $body -OutVariable optionList
    $id = ($optionList | convertfrom-json | select -ExpandProperty optionTypeList).id

    add-Input -name $name -fieldName $fieldName -description $description -type select -id $id -required $required