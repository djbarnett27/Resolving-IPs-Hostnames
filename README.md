This script can be used in a corporate or home environment with access to either internal or external DNS servers. 
The purpose of this script is to assist users with resolving IP addresses to their respective hostnames, or vice versa.
The user is required to supply one or more IP addresses and/or hostnames (fully qualified hostnames may be required) without any blank lines between them. 
The input stops once a blank line after user presses the enter key.
The script will run and display the DNS forward or reverse lookup information.
Afterwards, the script will ask if you would like to continue (press "y" key) or quit (press "n" key).

Paste IPs/hostnames (one per line). End with an empty line:

8.8.8.8
cnn.com

***Output***

Resolving input items:
8.8.8.8                                  -> dns.google
cnn.com                                  -> 151.101.3.5, 151.101.67.5, 151.101.131.5, 151.101.195.5

Do you want to continue? (y/N): 
