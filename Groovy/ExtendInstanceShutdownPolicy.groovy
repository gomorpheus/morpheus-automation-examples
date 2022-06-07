//groovy local task
//run on a instance in Morpheus to extend its defined shutdown date

def extendDays = 90 //extend shutdown date x days in future
def extendWarningDays = 30 // reveal shutdown extend button x days before shutdown
def i = com.morpheus.Instance.get(instance.id)
i.shutdownDate = new Date().plus(extendDays)
i.shutdownWarningSent = false
i.shutdownWarningDate = new Date().plus((extendDays - extendWarningDays))
try {
    i.save(flush:true)
    println "Success!"
} catch(e) {
    println "Failure!"
}
