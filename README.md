logincrack.py is a tool used to deploy SQL injection attacks against web authentication logins.

The thesis of this tool is that there are many attack vectors other than the traditional ones that must be tested against web logins, and there are no publicly available tools that probe logins with such attack vectors. The nature of these injections is explained at https://nzt-48.org/new-tool-for-authentication-bypass

Installation
Latest version of selenium must be installed. It can be installed with
pip install selenium


Usage:

logincrack.py -u USERNAME -t http://vulnerable.com/login_address


More cryptographic hashing functions such as nested functions and so on can be added to the script in the array declared at the beginning of the code.
