'''
Created on Oct 12, 2012

@author: vietht
'''

# import needed modules
import ldap
import ldap.modlist as modlist
import datetime

IP = "192.168.25.108"

begin = datetime.datetime.now()

# Open a connection
l = ldap.open(IP)

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=admin,dc=ming,dc=vn","convit")


for i in range(1680000, 2000001):

    mail="viet%s@ming.vn" % (i)
    
    # The dn of our new entry/object
    dn="mail=%s,ou=Users,domainName=ming.vn,o=domains,dc=ming,dc=vn" % (mail) 
    
    # A dict to help build the "body" of the object
    attrs = {}
    #attrs['objectclass'] = ['top','inetOrgPerson','shadowAccount','posixAccount']
    attrs['objectclass'] = 'inetOrgPerson'
    attrs['mail'] = mail
    attrs['cn'] = 'Test'
    attrs['sn'] = 'Test'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
    
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
    print i
    
# Its nice to the server to disconnect and free resources when done
l.unbind_s()

end = datetime.datetime.now()

print begin
print end
print end-begin