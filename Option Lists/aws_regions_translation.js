// This translation script takes all clouds in the environments that are of the type amazon and parses it to get unique values for all of the regions available.
// The return is an array of key value pairs [name=region,value=region]
// Source URL: https://{{Morph_URL}}/api/zones?type=amazon&max=10000

var results = [];
data = data.zones

function search(nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {
        if (myArray[i].name === nameKey) {
            return true;
        }else{
            return false
        }
    }
}

results.push(
   {
        name:data[0].regionCode.split(".")[1],
        value:data[0].regionCode.split(".")[1]
    }
)

for (var x = 1; x < data.length; x++) {
    region = data[x].regionCode.split(".")[1]
    if (search(region, results) === false){
        results.push(
            {
            name: region,
            value:region
            }
        );
    }
}