import com.morpheus.NetworkDomainService
import com.morpheus.PermissionService
import com.morpheus.NetworkDomain
import com.bertramlabs.plugins.Account
 
PermissionService permissionService
NetworkDomain networkDomain
def networkDomainName = NetworkDomain.findByName('test.morpheusdata.com')
println "Domain info"
println networkDomainName.id
println networkDomainName.name
 
def masterTenant = Account.where{'masterAccount' == true }.find()
println "Master tenant info"
println masterTenant.id
println masterTenant.name
 
def subTenant = Account.findByName('abc')
println "Subtenant info"
println subTenant.id
println subTenant.name
 
def tenantIds = []
println "Master tenant info"
tenantIds << masterTenant.id
tenantIds << subTenant.id
println tenantIds
 
def groupItems = customOptions.groupList
def groupStrg = []
groupStrg = groupItems.collect { ["id": it, "default": true] }
 
 
permissionService = grails.util.Holders.applicationContext['permissionService']
permissionService.updateTenantPermissions('NetworkDomain',networkDomainName.id, tenantIds.collect { it.toLong()} )
 
//def resourcePermissions = [all: false, sites: [[id: 70, default: true]] ]
def resourcePermissions = [all: false, sites: groupStrg]
permissionService.updateResourcePermissions(masterTenant, 'NetworkDomain', networkDomainName.id, resourcePermissions)
results.success