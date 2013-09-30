Invisible Internet
==================

The following need to be installed -

+ Database - Redis, Neo4j
+ Python - Redis, PublicSuffixList, trie, py2neo...

Running the tool - 

+ To do a prerun, type **./run.sh -p**. This will start the Redis server in the background.
+ To do a load, type **./run.sh -l**. This will load the IP-to-ASN map into Redis DB. Required only once.
+ To do a run, type **./run.sh -r**.
+ To do a clean up, type **./run.sh -c**.

As of now the tool has three phases -

+ **Phase One** - Preprocessing the traceroute and DNS files
+ **Phase Two** - Process the output from Phase One and make a best guess of physical infrastructure
+ **Phase Three** - If there are unfound router locations, suggest targetted probing
