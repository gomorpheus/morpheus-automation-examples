Function Connect-Morpheus ($URL, $Username) {

    ####  User Variables  ####
    if ($Username -eq $null) {
        $Username = Read-Host 'Enter Username'
        }
    $Password = Read-host 'Enter your password' -AsSecureString
    $PlainTextPassword= [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR( ($Password) ))

    ####  Morpheus Variables  ####
    $Body = "username=$Username&password=$PlainTextPassword"
    $URL = Read-Host 'Enter Morpheus URL'
    $AuthURL = "/oauth/token?grant_type=password&scope=write&client_id=morph-customer"

    ####  Create User Token   ####
    $Token = Invoke-WebRequest -Method POST -Uri ($URL + $AuthURL) -Body $Body | select -ExpandProperty content|
        ConvertFrom-Json | select -ExpandProperty access_token
    $Header = @{
        "Authorization" = "BEARER $Token"
        }

    return $Header
}