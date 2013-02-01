'''
Created on Jan 30, 2013

@author: vietht
'''

import ldap
import datetime
from random import randint

## The next lines will also need to be changed to support your search requirements and directory
baseDN = "ou=Users,domainName=ming.vn,o=domains,dc=ming,dc=vn"
MIN = 1
MAX = 2000000 

# Read parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="LDAP Server's IP")
parser.add_argument("--mailnumber", help="Mail quantity")
parser.add_argument("--debug", help="0 or 1")
args = parser.parse_args()

# Default values
if args.ip:
    IP = args.ip
else:
    IP = "localhost"
if args.mailnumber:
    MAIL_NUMBER = int(args.mailnumber)
else:
    MAIL_NUMBER = 2
if args.debug:
    DEBUG = bool(int(args.debug))
else:    
    DEBUG = False

def test(mail_no):
    
    ## first you must open a connection to the server
    try:
        l = ldap.open(IP)
        ## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
        ## and do a bind as shown in the above example.
        # you can also set this to ldap.VERSION2 if you're using a v2 directory
        # you should  set the next option to ldap.VERSION2 if you're using a v2 directory
        l.protocol_version = ldap.VERSION3    
    
        # DEBUG        
        begin = datetime.datetime.now()
        
        searchScope = ldap.SCOPE_ONELEVEL
        ## retrieve all attributes - again adjust to your needs - see documentation for more options
        retrieveAttributes = None
        mail = "viet%s@ming.vn" % (mail_no)
        
        if DEBUG:
            print "Searching %s.." % (mail)
            
        searchFilter = "mail=%s" % (mail)
        
        # async search
        try:
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    ## here you don't have to append to a list
                    ## you could do whatever you want with the individual entry
                    ## The appending to list is just for illustration. 
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            if DEBUG:
                print result_set
        except ldap.LDAPError, e:
            print e    

#        # sync search        
#        try:
#            ldap_result = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
#            if DEBUG:                
#                print ldap_result
#        except ldap.LDAPError, e:
#            print e
#    
#        end = datetime.datetime.now()
#        
#        if DEBUG:
#            print "Search time is: %s" % (end - begin)
#    
#    except ldap.LDAPError, e:
#        print e
#        # handle error however you like
    
########################################################################
# Test case 1: search MAIL_NUMBER mails randomly
########################################################################
def tc1():
    print "################################################################################" 
    print "# Test case 1: search %s mail(s) randomly" % (MAIL_NUMBER)
    print "################################################################################" 
    
    begin = datetime.datetime.now()
    
    for i in range(0, MAIL_NUMBER):
        mail_no = randint(MIN, MAX)
        test(mail_no)    
        
    end = datetime.datetime.now()
    
    report(begin, end, MAIL_NUMBER)
    
########################################################################
# Test case 2: search MAIL_NUMBER non-existent mails randomly
########################################################################

def tc2():
    print "################################################################################"    
    print "# Test case 2: search %s non-existent mail(s) randomly"  % (MAIL_NUMBER)    
    print "################################################################################"
    
    begin = datetime.datetime.now()
    
    for i in range(0, MAIL_NUMBER):
        mail_no = randint(MAX, MAX * 2)
        test(mail_no)    
        
    end = datetime.datetime.now()
    
    report(begin, end, MAIL_NUMBER)
    
def report(begin, end, query_number):
    
    time = (end-begin)/query_number
    print "Average search time is: %s" %(time)

def main():
    tc1()
    tc2()

if __name__ == '__main__':
    main()