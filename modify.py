'''
Created on Oct 12, 2012

@author: tivalat
'''
# import needed modules
import ldap

# Open a connection
l = ldap.open("127.0.0.1")

# Bind/authenticate with a user with appropriate rights to add objects
l.simple_bind_s("cn=admin,dc=ming,dc=vn","test")

# The dn of our existing entry/object
dn="uid=minh,ou=Users,dc=ming,dc=vn" 

mod_attrs = [
( ldap.MOD_REPLACE, 'userPassword', 'minh123' ),
( ldap.MOD_REPLACE, 'sambaNTPassword', 'minh123' )
]

# Do the actual modification 
l.modify_s(dn,mod_attrs)

# Its nice to the server to disconnect and free resources when done
l.unbind_s()