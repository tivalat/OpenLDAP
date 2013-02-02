'''
Created on Jan 30, 2013

@author: vietht
'''

import ldap
import datetime
from random import randint

# Constants
baseDN = "ou=Users,domainName=ming.vn,o=domains,dc=ming,dc=vn"
MIN = 1
MAX = 2000000
LOG = '' 
TC = 1

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

########################################################################
# Test case 1: search MAIL_NUMBER mails randomly
########################################################################
import Queue
def tc1(ldap_conn, does_mail_exist):
    print "################################################################################" 
    print "# Test case 1: search %s mail(s) randomly" % (MAIL_NUMBER)
    print "################################################################################" 
    
    begin = datetime.datetime.now()
    ldap_result = Queue.Queue()
        
    # async search
    try:
        for i in range(0, MAIL_NUMBER):
            if does_mail_exist:
                mail_no = randint(MIN, MAX)
            else:
                mail_no = randint(MAX, MAX*2)
        
            searchScope = ldap.SCOPE_ONELEVEL
            ## retrieve all attributes - again adjust to your needs - see documentation for more options
            retrieveAttributes = None
            mail = "viet%s@ming.vn" % (mail_no)
        
            if DEBUG:
                print "Searching %s..." % (mail)
                
            searchFilter = "mail=%s" % (mail)
            ldap_result.put(ldap_conn.search(baseDN, searchScope, searchFilter, retrieveAttributes))
            
        while not ldap_result.empty():
            result_set = []
            ldap_result_id = ldap_result.get()
            
            while 1:
                result_type, result_data = ldap_conn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    ## here you don't have to append to a list
                    ## you could do whatever you want with the individual entry
                    ## The appending to list is just for illustration. 
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
                
                # DEBUG
                if DEBUG:
                    print "Result: %s" % (result_set)
                
    except ldap.LDAPError, e:
        print e     
        
    end = datetime.datetime.now()
    report(begin, end, MAIL_NUMBER)
    
def report(begin, end, query_number):
    global TC, LOG
    
    time = (end-begin)/query_number
    log = "Test case %s: Searched %s entries. Average search time is: %s" %(TC, query_number, time)
    TC += 1
    LOG += log + "\n"

def main():
    
    # first you must open a connection to the server
    try:
        ldap_conn = ldap.open(IP)
        ## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
        ## and do a bind as shown in the above example.
        # you can also set this to ldap.VERSION2 if you're using a v2 directory
        # you should  set the next option to ldap.VERSION2 if you're using a v2 directory
        ldap.protocol_version = ldap.VERSION3  
        tc1(ldap_conn, 1)
        tc1(ldap_conn, 0)
        print LOG
    except ldap.LDAPError, e:
        print e
        # handle error however you like

if __name__ == '__main__':
    main()