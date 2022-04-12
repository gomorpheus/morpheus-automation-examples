// This translation script takes the current user and runs an ldap query to return the selected attribute
// The return is an array of key value pairs [name=attribute_value,value=attribute_value]
// LDAP Query (objectClass=user)

if(input.user != null) {
    for(var x=0;x < data.length ; x++) {
        var attrib = "department"
        var row = data[x];
        var a = {};
        if(row.sAMAccountName === input.user.username) {
          if(row[attrib] != null) {
          a['name'] = row[attrib];
        } else {
          a['name'] = row[attrib];
        }
        a['value'] = row[attrib];
        results.push(a);
        }
    }
}
