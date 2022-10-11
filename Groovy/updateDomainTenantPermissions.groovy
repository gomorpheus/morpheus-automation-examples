import com.morpheus.NetworkDomainService
import com.morpheus.PermissionService
import com.morpheus.NetworkDomain
import com.bertramlabs.plugins.Account

PermissionService permissionService
NetworkDomain networkDomain
// Get the object of the Network Domain
def networkDomainName = NetworkDomain.findByName('test.morpehusdata.com')
println networkDomainName.id
println networkDomainName.name

// Get the master tenant object
def masterTenant = Account.where{'masterAccount' == true }.find()
println masterTenant.id
println masterTenant.name

// Get sub tenant object
def subTenant = Account.findByName('')
println subTenant.id
println subTenant.name

def tenantIds = []
tenantIds << masterTenant.id
tenantIds << subTenant.id
println tenantIds

// Initialize global application Context for permissionService
permissionService = grails.util.Holders.applicationContext['permissionService']
permissionService.updateTenantPermissions('NetworkDomain',networkDomainName.id, tenantIds.collect { it.toLong()} )

// Update group permissions for the network domain
def resourcePermissions = [all: false, sites: [[id: 70, default: true]] ]
permissionService.updateResourcePermissions(masterTenant, 'NetworkDomain', networkDomainName.id, resourcePermissions)
results.success