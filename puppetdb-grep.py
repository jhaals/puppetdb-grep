#!/usr/bin/env python
# Created by Johan Haals https://github.com/jhaals

# Queries puppetdb with a grep superpowers.

# Make sure to change SERVER to the correct URL for your system
# The default SERVER should work if you run this locally on your puppetdb server.

import sys
import json
try:
    import requests
except ImportError:
    sys.exit('requests is not installed. Run: pip install requests')
from optparse import OptionParser

SERVER = 'http://localhost:8080'


usage = '''usage: %prog -h
Example Queries:

Query active nodes for their puppetversion
    puppetdb-grep.py --query '["=", ["node", "active"], True]' --grep puppetversion

Query active nodes with app_microsoftword and location Stockholm, grep for app_microsoftword_version
    puppetdb-grep.py --query '[ "and", ["=", ["node", "active"], True],
        ["=", ["fact", "kernel"], "Darwin"],
        ["=", ["fact", "app_microsoftword"], True]]' --grep app_microsoftword_version

Query for all active nodes with kernel Linux
    puppetdb-grep.py --query '["and", ["=", ["node", "active"], True], ["=", ["fact", "kernel"], "Linux"]]'
'''
parser = OptionParser(usage)
parser.add_option('--query', help='Puppetdb query', default=False)
parser.add_option('--grep', help='Grep this fact from matching nodes', default=False)

options, args = parser.parse_args()

result = {}
url = '%s/nodes' % SERVER
headers = {'Accept': 'application/json'}

def grep(node, grep):
    """
    Query node for all facts, fetch specific fact.
    """
    url = '%s/facts/%s' % (SERVER, node)
    r = requests.get(url, headers=headers, verify=False)
    try:
        # adds : to YAML format the output
        fact = r.json['facts'][grep]+':'
        if not result.has_key(fact):
            result[fact] = []
        result[fact].append(node)
    except KeyError:
        # The fact we want does not exist on this node, skip.
        pass
    return result

if not options.query:
    parser.error('You must query for something!')

if options.query:

    try:
        payload = { 'query': json.dumps(eval(options.query))}
    except SyntaxError:
        parser.error('Malformed query, check examples for help')

    r = requests.get(url, headers=headers, params=payload, verify=False)

    # Loop the result node by node
    for node in r.json:

        if options.grep:
            grep(node, options.grep)
        else:
            print node

    if options.grep:
        for value, nodes in result.iteritems():
            print value
            for node in nodes:
                print '- %s' % node
