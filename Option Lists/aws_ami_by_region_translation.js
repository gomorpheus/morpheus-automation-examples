// This translation script takes the input from the option type tied to the aws_regions_translation.js and uses the selected region to get the amis based on said selection
// The return is an array of key value pairs [name=ami_id,value=ami_id]
// Source URL: https://{{Morph_URL}}/api/virtual-images?imageType=ami&filterType=All&max=10000

var results = [];
data = data.virtualImages
region = input.awsRegion

function search(nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {
        if (myArray[i].name === nameKey) {
            return true;
        }else{
            return false
        }
    }
}

for (var x = 0; x < data.length; x++) {
    if (data[x].locations.length > 0) {
    locations = data[x].locations
        for (var y = 0; y < locations.length; y++){
            location = locations[y]
            if (location.imageRegion === region){
                results.push(
                    {
                        name: location.imageName,
                        value: location.externalId
                    }
                );
            }
        }
    }else{
        results.push(
            {
                name: data[x].name,
                value: data[x].externalId
            }
        )
    }
}