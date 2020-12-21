def owner = com.bertramlabs.plugins.Account.get(1)
def dcServer = container.server.hostname
if(dcServer.contains('.')) {
dcServer = dcServer.tokenize('.')[0]
}

def description
if(instance.apps) {
description = "Created from App: ${instance.apps.first().name}"
}
def networkDomain = new com.morpheus.NetworkDomain(name:customOptions.domainName, description: description, owner: owner, domainController: true, domainUsername: 'Administrator', domainPassword: 'bertram4Admin!', dcServer: instance.name, account: owner, refType: 'Instance', refId: instance.id)

networkDomain.save(flush:true,failOnError:true)

def networkId = container.networkInterfaces ? container.networkInterfaces.first().network?.id?.toLong() : null

println "Interface Config: ${container.networkInterfaces.first()}"
println "NETWORK DETECTED: ${networkId}"
if(networkId) {

def network = com.morpheus.Network.get(networkId)
network.networkDomain = networkDomain
network.dnsPrimary = container.externalIp
network.save(flush:true)

}