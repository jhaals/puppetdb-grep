# puppetdb-grep

puppetdb-grep gives you the ability to for example get all puppetversions for active nodes running Linux.

_This is just a quick evening hack I did, don't expect any magic unicorns!_

Please note that some queries are expensive since puppetdb-grep asks all nodes matching your query for their --grep __fact__

Examples:
---

__Give me all active nodes:__

    puppetdb-grep.py --query '["=", ["node", "active"], True]'

__Give me all active nodes and their puppetversion__

    puppetdb-grep.py --query '["=", ["node", "active"], True]' --grep puppetversion


Query active nodes with kernel Linux with uptime greater then 30, grep for their memorytotal

    puppetdb-grep.py --query '["and",
        ["=", ["node", "active"], True],
        ["=", ["fact", "kernel"], "Linux"],
        [">", ["fact", "uptime_days"], 30]]' --grep memorytotal

Example Output:

    $ puppetdb-grep.py --query '
        ["and",["=", ["node", "active"], True],
        ["=", ["fact", "Linux"], "Darwin"],
        [">", ["fact", "uptime_days"], 30]]' --grep puppetversion
    2.7.18:
    - node1.example.com
    - node.32.example.com
    2.7.19:
    - node139.example.com
    - node75.example.com
