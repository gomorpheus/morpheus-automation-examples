// The script will set the disk label at the instance level to root for root disk if the name is not root
def computeServerObj = com.morpheus.ComputeServer.get(server.id)
def serverVolumes = computeServerObj.volumes?.sort { it.displayOrder }
for (int i = 0; i < 1; i++) {
        def volume = serverVolumes[i]
            if (volume.name != "root") {
                // change and save
                volume.name = "root"
                println "Renaming mount point : ${volume.name}"
                volume.save(flush:true, failOnError:true)
            }
    }