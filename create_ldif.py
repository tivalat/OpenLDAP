file = open('users.ldif', 'w')

MAX = 2000000

for i in range(1, MAX + 1):
    user = "viet%s" %(i)
    file.write("dn: mail=%(user)s@ming.vn,ou=Users,domainName=ming.vn,o=domains,dc=ming,dc=vn\n\
objectClass: inetOrgPerson\n\
mail: %(user)s@ming.vn\n\
cn: Test\n\
sn: Test\n\n\
" % {"user" : user})
    
file.close()