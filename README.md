Invisible Internet
==================

The following need to be installed -

+ Database - Redis
+ Python - Redis, PublicSuffixList, trie...

Running the tool - 

+ To do a prerun, type *./run.sh -p*. This will start the Redis server in the background.
+ To do a load, type *./run.sh -l*. This will load the IP-to-ASN map into Redis DB. Required only once.
+ To do a run, type *./run.sh -r*.
+ To do a clean up, type *./run.sh -c*.
