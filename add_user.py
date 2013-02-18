'''
Created on Oct 12, 2012

@author: vietht
'''

# import needed modules
import ldap
import ldap.modlist as modlist
import datetime

IP = "192.168.25.108"
MIN = 1
MAX = 1

# Read parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="LDAP Server's IP")
parser.add_argument("--debug", help="0 or 1")
parser.add_argument("--min")
parser.add_argument("--max")
args = parser.parse_args()

# Default values
if args.ip:
    IP = args.ip
else:
    IP = "localhost"
if args.debug:
    DEBUG = bool(int(args.debug))
else:    
    DEBUG = False
if args.min:
    MIN = args.min
if args.max:
    MAX = args.max    

begin = datetime.datetime.now()

# Open a connection
l = ldap.open(IP)

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=admin,dc=ming,dc=vn","convit")

# Add base
try:
    dn = "dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = ['dcObject', 'organization']
    attrs['dc'] = 'ming'
    attrs['o'] = 'Example Corporation'
    attrs['description'] = 'The Example Corporation'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e
    
try:
    dn = "cn=admin,dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = 'organizationalRole'
    attrs['cn'] = 'admin'
    attrs['description'] = 'Directory Manager'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e
    
try:
    dn = "cn=admin,dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = 'organizationalRole'
    attrs['cn'] = 'admin'
    attrs['description'] = 'Directory Manager'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e
    
try:
    dn = "o=domains,dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = ['top', 'organization']
    attrs['o'] = 'domains'
    attrs['l'] = 'o=domains,dc=ming,dc=vn'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e
    
try:
    dn = "domainName=ming.vn,o=domains,dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = ['top', 'mailDomain']
    attrs['domainName'] = 'ming.vn'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e
    
try:
    dn = "domainName=ming.vn,o=domains,dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = ['top', 'mailDomain']
    attrs['domainName'] = 'ming.vn'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e

try:
    dn = "ou=Users,domainName=ming.vn,o=domains,dc=ming,dc=vn"
    
    attrs = {}
    attrs['objectClass'] = ['top', 'organizationalUnit']
    attrs['ou'] = 'Users'
    
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
        
    # Do the actual synchronous add-operation to the ldapserver
    l.add_s(dn,ldif)
except Exception, e:
    print e

# Add users
for i in range(MIN, MAX+1):
    try:
        mail = "viet%s@ming.vn" % (i)
        
        # The dn of our new entry/object
        dn = "mail=%s,ou=Users,domainName=ming.vn,o=domains,dc=ming,dc=vn" % (mail) 
        
        # A dict to help build the "body" of the object
        attrs = {}
        attrs['objectClass'] = 'inetOrgPerson'
        attrs['mail'] = mail
        attrs['cn'] = 'Test'
        attrs['sn'] = 'Test'
        
        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = modlist.addModlist(attrs)
        
        # Do the actual synchronous add-operation to the ldapserver
        l.add_s(dn,ldif)
        print i
    except Exception, e:
        print e
    
# Its nice to the server to disconnect and free resources when done
l.unbind_s()

end = datetime.datetime.now()

print begin
print end
print end-begin