import sys
import re
from publicsuffix import PublicSuffixList
import trie
import redis

## TODO
## Peering Information
## Physical data information from Atlas
## Add interpolation logic -- best guess

## City trie 
psl = PublicSuffixList()
city_dict_io = open('dictionary.dat','r')
city_trie = trie.Trie()
for cities in city_dict_io:
    tmp = cities.rstrip().lower()
    if len(tmp) > 3:
        city_trie[tmp] = 0

## Map lookup -- code to city map
locMap = {}
with open('FullMap.txt','r') as mapFile:
    for line in mapFile:
        values = line.strip().split('--')
        key = re.sub(r'\s+','',values[0])
        ll = values[1][1:-1]
        keys = key.split(",")
        for k in keys:
            locMap[k] = ll

## Redis handle
redisHandle = redis.Redis("localhost")
def getASN(line_report_entries):
    pipe = redisHandle.pipeline() 
    for entry in line_report_entries:
        pipe.get(entry['IP'])
    values = pipe.execute()
    return values

def getLocation(hop):
    location = []
    for i in range(len(hop)):
        for j in range(0,31):
            if i+j > len(hop):
                break
            to_test = hop[i:i+j]
            try:
                i = city_trie[to_test.lower()]
                location.append(to_test)
            except trie.NeedMore:
                continue
            except KeyError:
                continue
            except:
                continue
    return ','.join(location)

def processFiles(dnsFile,trFile):
    dns_to_ip = {}
    total_hops = 0
    name_coverage = 0
    
    print "Processing DNS"
    f=open(dnsFile,'r')
    for lines in f:
        strs = lines.split('\t')
        t_ip = strs[1].rstrip().lower()
        t_dns = strs[2].rstrip().lower()
        if ("non-authoritative" not in t_dns) and ("timeout" not in t_dns) and ("in-addr.arpa" not in t_dns) and ("server-failure" not in t_dns):
            dns_to_ip[t_ip] = t_dns
        else:
            dns_to_ip[t_ip] = "NULL"
       
    print "Processing Traceroute"
    g = open(trFile,'r')
    reg_hop = re.compile('\d+[.]\d+[.]\d+[.]\d+[,]\d+')
    for lines in g:
        strs = lines.split('\t')
        report_line_entries = []
        for entries in strs:
            entry = {}
            if reg_hop.findall(entries):
                e2 = entries.split(',')
                total_hops += 1
                if e2[0] in dns_to_ip:
                    name_coverage += 1
                    entry['IP'] = e2[0]
                    hop = dns_to_ip[e2[0]]
                    entry['DNS'] = hop
                    entry['NAME'] = psl.get_public_suffix(hop)
                    entry['GEO'] = getLocation(hop)
                    entry['ASN'] = ''
                else:
                    entry['IP'] = e2[0]
                    entry['ASN'] = ''
                report_line_entries.append(entry)
        asnValues = getASN(report_line_entries)
        index = 0
        for entries in report_line_entries:
            entries['ASN'] = asnValues[index]
            index += 1
        print report_line_entries
        print "\n"
    print "There are %d dns names on record" %(len(dns_to_ip))
    print "Total network hops: %d" %(total_hops)
    print "Total resoved hops: %d" %(name_coverage)

if __name__ == '__main__':
    dnsFile = sys.argv[1]
    trFile = sys.argv[2]
    processFiles(dnsFile,trFile)
