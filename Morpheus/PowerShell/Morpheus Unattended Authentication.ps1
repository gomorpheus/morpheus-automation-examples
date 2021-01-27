### Morpheus Variables ###
$MorphURL = "https://url.com"
$serviceBearer = 'bearertoken' # Insert user API token
$morphHeader = @{
    "Authorization" = "BEARER $serviceBearer"
    }
$ContentType = 'application/json'

(Invoke-WebRequest -Method Get -Uri ($MorphURL + $endpoint) -Headers $Header).content | ConvertFrom-Json