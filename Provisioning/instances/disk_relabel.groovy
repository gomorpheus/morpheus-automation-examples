import groovy.json.*

// the JSON pasted body
def jsonBody = customOptions.fjJSONBody

def computeServerObj = com.morpheus.ComputeServer.get(server.id)

//get current server volume information ordered by the displayOrder
def serverVolumes = computeServerObj.volumes?.sort { it.displayOrder }

// capture & parse the JSON to a list
def data = new JsonSlurper().parseText(jsonBody)

// iterate the list
for (int i = 0; i < data.disks.size(); i++) {
    def disk = data.disks[i]
    for (int ii = 0; ii < serverVolumes.size(); ii++) {
        def volume = serverVolumes[ii]
        def morphMount = volume.getMountPointName()
        if (disk.mount == morphMount) {
            // inspect the volume name and compared to required (disk.label)
            if (volume.name != disk.label) {
                // change and save
                println "Renaming mount point : `${morphMount}` to `${disk.label}`"
                volume.name = disk.label
                volume.save(flush:true, failOnError:true)
            }
        }
    }
}