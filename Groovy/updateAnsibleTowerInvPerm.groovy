import com.morpheus.AccountInventory
import com.morpheus.automation.AnsibleService
import com.morpheus.PermissionService
import com.bertramlabs.plugins.Account

PermissionService permissionService
AccountInventory inventory
def inventoryName = AccountInventory.findByName('Windows')
println inventoryName.id
println inventoryName.name

def masterTenant = Account.where{'masterAccount' == true }.find()
println masterTenant.id
println masterTenant.name

def subTenant = Account.findByName('Customer Tenant Test01')
println subTenant.id
println subTenant.name

def tenantIds = []
tenantIds << masterTenant.id
tenantIds << subTenant.id
println tenantIds

permissionService = grails.util.Holders.applicationContext['permissionService']
permissionService.updateTenantPermissions('AccountInventory', inventoryName.id, tenantIds.collect { it.toLong()})