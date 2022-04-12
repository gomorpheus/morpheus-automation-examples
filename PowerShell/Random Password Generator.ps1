function Get-RandomCharacters($length, $characters)
{
    $random = 1 .. $length | ForEach-Object { Get-Random -Maximum $characters.length }
    $private:ofs = ""
    return [String]$characters[$random]
}
 
function Scramble-String([string]$inputString)
{
    $characterArray = $inputString.ToCharArray()
    $scrambledStringArray = $characterArray | Get-Random -Count $characterArray.Length
    $outputString = -join $scrambledStringArray
    return $outputString
}
# Generate a random password
# Usage: random-password 
Function random-password {
    $password = Get-RandomCharacters -length 8 -characters 'abcdefghiklmnoprstuvwxyz'
    $password += Get-RandomCharacters -length 8 -characters 'ABCDEFGHKLMNOPRSTUVWXYZ'
    $password += Get-RandomCharacters -length 4 -characters '1234567890'
    $password += Get-RandomCharacters -length 3 -characters '!%/()=}][{@#+'
 
    $password = Scramble-String $password
    return $password
}