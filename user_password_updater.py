'''
LDAP password change utility

Created on Oct 12, 2012

@author: Viet Hoang

Require: 
        ldap
            sudo apt-get install python-ldap
        smbpasswd
            pip install smbpasswd

'''

# import needed modules
import ldap
import smbpasswd
import hashlib
import subprocess, sys, string, random
from getpass import getpass

def main():
    global BASE, ADMIN, ADMIN_PASSWD, HOST
    global l, md5_hash, NT_hash, user_dn, new_passwd, user_sid, sid, user, debug
    
    debug = 0
    
    HOST = "127.0.0.1"
    BASE = "dc=ming,dc=vn"
    ADMIN = "cn=admin," + BASE
    ADMIN_PASSWD = "test"
    
#    # Get root sambaSID, 
#    # NOTE: must run under root privilege
#    sid = get_local_SID()
    
    # DEBUG
    sid = "S-1-5-21-2412927883-13013413-872442205"
    
    # Get username and new password
    args = sys.argv[1:]
    if '-u' in args:
        try:
            user = args[1]
        except:
            usage()
    elif '-h' in args:
        usage()
    else:
        user = raw_input("Enter username: ")
    
    new_passwd = get_passwd()
    user_dn = "uid=" + str(user) + ",ou=Users," + BASE
    
#    # DEBUG
#    user = "minh"
#    user_dn = "uid=" + str(user) + ",ou=Users," + BASE
#    new_passwd = "minh"
    
    # Connect to ldap
    l = connect_to_ldap()
    
    # Get user UID
    uid = get_user_Unix_UID(user)
        
    # Calculate user sambaSID
    user_sid = sid + '-' + str(int(uid) * 2 + 1000)
    
    # Add sambaSamAccount object class ( for sambaNTPassword attribute )
    add_sambaSamAccount_object_class()
    
    # Modify password attributes 
    modify_password_attrs()
    
# Add sambaSamAccount object class ( for sambaNTPassword attribute )
def add_sambaSamAccount_object_class():
    mod_attrs = [
    (ldap.MOD_ADD, 'objectClass', ['sambaSamAccount']),
    (ldap.MOD_REPLACE, 'sambaSID', user_sid)
    ]
    
    try: 
        l.modify_s(user_dn, mod_attrs)
        print "Added sambaSamAccount object class"
    except ldap.TYPE_OR_VALUE_EXISTS:
        if debug:
            print "sambaSamAccount object class already exists. Not add."
        
def modify_password_attrs():
    # Hash password
    md5_hash = hash_passwd(new_passwd, "MD5")
    NT_hash = hash_passwd(new_passwd, "NT")
    mod_attrs = [
    (ldap.MOD_REPLACE, 'userPassword', md5_hash),
    (ldap.MOD_REPLACE, 'sambaNTPassword', NT_hash)
    ]
    
    try:
        l.modify_s(user_dn, mod_attrs)
        print "userPassword is updated"
        print "sambaNTPassword is updated"
        print "Changed password for user %s successfully" % user
    except Exception,e:
        print "Error when modify password attributes"
        print "ERROR: %s" % e
    
def hash_passwd(passwd, hash_type):
    import base64
    hash_type = hash_type.upper()
    if hash_type == "MD5":
        m = hashlib.md5()
        m.update(passwd)
        md5_hash = '{MD5}' + base64.encodestring(m.digest())
        return md5_hash
    elif hash_type == "SMD5":
        m = hashlib.md5()
        salt = get_salt()
        m.update(passwd + salt)
        md5_hash = '{SMD5}' + base64.encodestring(m.digest() + salt)
        return md5_hash
    elif hash_type == "SHA":
        m = hashlib.sha1()
        m.update(passwd)
        sha_hash = '{SHA}' + base64.encodestring(m.digest())
        return sha_hash
    elif hash_type == "SSHA":
        m = hashlib.sha1()
        salt = get_salt()
        m.update(passwd + salt)
        ssha_hash = '{SSHA}' + base64.encodestring(m.digest() + salt)
        return ssha_hash
    elif hash_type == "NT":
        NT_hash = smbpasswd.nthash(passwd)
        return NT_hash
    
def get_local_SID():
    try:
        output = subprocess.check_output(['net','getlocalsid'])
        output = output.split("is: ")
        sid = output[1].strip()
        return sid
    except Exception,e:
        print "ERROR: %s" % e
        sys.exit(1)
        
def connect_to_ldap():
    try:
        # Open a connection
        l = ldap.open(HOST)
        
        # Bind admin user
        l.simple_bind_s(ADMIN,ADMIN_PASSWD)
        
        return l
    except Exception,e:
        print "Error when connecting to LDAP server"
        print "ERROR: %s" % e
        sys.exit(1)
        
def get_user_Unix_UID(user):
    base = "ou=Users," + BASE
    scope = ldap.SCOPE_ONELEVEL
    filterstr = "(uid=%s)" % user
    attrlist = ["uidNumber"]
        
    try:  
        result = l.search_s(base, scope, filterstr, attrlist)
    except Exception,e:
        print "ERROR: %s" % e
        
    try:
        uid = result[0][1]['uidNumber'][0]
        uid = uid.strip()
        return uid
    except Exception,e:
        print "User %s does not exist" % user
        print "ERROR: %s" % e
        sys.exit(1)
    
def get_salt(chars = string.letters + string.digits, length = 16):
    """Generate a random salt. Default length is 16.
    """
    salt = ""
    for i in range(int(length)):
        salt += random.choice(chars)
    return salt
        
def get_passwd():
    p1 = getpass("Enter new password: ")
    p2 = getpass("Confirm new password: ")
    if p1 != p2:
        print "Passwords mismatch"
        sys.exit(1)
    return p1
        
def usage():
    print "LDAP password updater"
    print "To change user\'s password with prompts:"
    print "    %s" % sys.argv[0]
    print "Or use:"
    print "    %s -u <username>" % sys.argv[0]
    print "Help:"
    print "    %s -h" % sys.argv[0]
    print ""
    sys.exit()
        
if __name__ == '__main__':
    main()