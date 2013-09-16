#!/bin/bash

outFile="/scratch/SIGCOMM14/Output/IPtoASN3.txt"
while read line
do
    whois -h whois.cymru.com " -f -o $line" |sed -n 3p >> $outFile
    sleep 0.1
done < "/scratch.1/AllSeenIPs/AllSeenIPs2.txt"
#echo "Mapping done!" | mail -s "IP to ASN" rkrish@cs.wisc.edu
