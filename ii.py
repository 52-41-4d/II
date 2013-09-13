import sys
import re
from publicsuffix import PublicSuffixList
import trie
import redis

## TODO
## Add ASN mapping - use REDIS?
## Peering Information
## Physical data information from Atlas
## Add interpolation logic -- best guess
## Do a redis pipeline for an entire traceroute probe to improve lookup performance

## City trie 
psl = PublicSuffixList()
city_dict_io = open('dictionary.dat','r')
city_trie = trie.Trie()
for cities in city_dict_io:
    tmp = cities.rstrip().lower()
    if len(tmp) > 3:
        city_trie[tmp] = 0

## Map lookup
locMap = {}
with open('FullMap.txt','r') as mapFile:
    for line in mapFile:
        values = line.strip().split('--')
        key = re.sub(r'\s+','',values[0])
        ll = values[2][1:-1]
        keys = key.split(",")
        for k in keys:
            locMap[k] = ll

## Redis handle
redisHandle = redis.Redis("localhost")

def getASN(IP):
    value = redisHandle.get(IP)
    if value:
        ASN="ASN:%s" % (value)
    else:
        ASN="ASN:NULL"
    return ASN

# Link this module with withDNS function and avoid three character only lookups
def lookupFromMap(hopValue):
    location = "NULL"
    location = locMap[hopValue]
    return location    

def withDNS(IPandDNS):
    values = []
    tVal = IPandDNS.split(',')
    IP = tVal[0]
    DNS = tVal[1] 
    values.append("IP:%s" % (IP))
    values.append(DNS)
    hop = DNS.split(':')[1]
    name = psl.get_public_suffix(hop)
    values.append("NAME:%s" % (name))
    hit = 0
    for i in range(len(hop)):
        for j in range(0,31):
            if i+j > len(hop):
                break
            to_test = hop[i:i+j]
            try:
                city_trie[to_test.lower()]
                values.append("GEO:%s" % (to_test))
                hit = 1
            except trie.NeedMore:
                continue
            except KeyError:
                continue
            except:
                continue
            if hit == 0:
                values.append("GEO:NULL")
    values.append(getASN(IP))
    return values

def withoutDNS(IP):
    values = []
    values.append("IP:%s" % (IP))
    values.append("DNS:NULL")
    values.append(getASN(IP))
    return values

def addDetails(lines):
    reg_hop = re.compile('\d+[.]\d+[.]\d+[.]\d+[,]DNS:')
    resultHops = []
    for hop in lines:
        if reg_hop.findall(hop):
            resultHops.append(str(withDNS(hop)))
        else:
            resultHops.append(str(withoutDNS(hop)))
    return resultHops

def processFiles(dnsFile,trFile):
    f=open(dnsFile,'r')

    dns_to_ip = {}
    total_hops = 0
    name_coverage = 0
    
    print "Processing DNS"
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
    dns_names = []
    for lines in g:
        strs = lines.split('\t')
        report_line_entries = []
        for entries in strs:
            if reg_hop.findall(entries):
                e2 = entries.split(',')
                total_hops += 1
                if e2[0] in dns_to_ip:
                    name_coverage += 1
                    report_line_entries.append("%s,DNS:%s" % (e2[0],dns_to_ip[e2[0]]))
                else:
                    report_line_entries.append("%s" % (e2[0]))
        resultHops = addDetails(report_line_entries)
        print ",".join(resultHops)
    print "There are %d dns names on record" %(len(dns_to_ip))
    print "Total network hops: %d" %(total_hops)
    print "Total resoved hops: %d" %(name_coverage)

if __name__ == '__main__':
    dnsFile = sys.argv[1]
    trFile = sys.argv[2]
    processFiles(dnsFile,trFile)
