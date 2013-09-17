import sys
import re
from publicsuffix import PublicSuffixList
import trie
import redis

## TODO
## Add pickle/json dump so that Phase two can use this output
## Add D2L mapping

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
    seen = 0
    hit = 0
    for i in range(len(hop)):
        for j in range(0,31):
            if i+j > len(hop):
                break
            to_test = hop[i:i+j]
            try:
                if seen==0 and hit==0:
                    city_trie[to_test.lower()]
                    location.append(to_test)
                    hit = 1
            except:
                try:
                    loc = locMap[to_test]
                    if loc and seen==0 and hit==0:
                        location.append(loc.split(',')[0].lower())
                        seen = 1
                    else:
                        continue
                except:
                    continue
    return ','.join(location)

def withDNS(ip):
    entry = {}
    entry['IP'] = ip
    hop = dns_to_ip[ip]
    entry['DNS'] = hop
    entry['NAME'] = psl.get_public_suffix(hop)
    entry['GEO'] = re.sub(r'\s','',getLocation(hop))
    entry['ASN'] = ''
    return entry

def withoutDNS(ip):
    entry = {}
    entry['IP'] = ip
    entry['ASN'] = ''
    return entry

def processFiles(dnsFile,trFile,jsonFile):
    global dns_to_ip
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
    end_node = re.compile('\d+[.]\d+[.]\d+[.]\d+$')
    reg_hop = re.compile('\d+[.]\d+[.]\d+[.]\d+[,]\d+')

    #appends source-hops-destination to a dictionary
    for lines in g:
        strs = lines.split('\t')
        report_line_entries = []
        sdIndex = 0
        source = ''
        destination = ''
        hops = 0
        for entries in strs:
            entry = {}
            hops += 1
            if end_node.findall(entries):
                total_hops += 1
                if sdIndex == 0:
                    source = entries
                    if source in dns_to_ip:
                        name_coverage += 1
                        report_line_entries.append(withDNS(source))
                    else:
                        report_line_entries.append(withoutDNS(source))
                if sdIndex == 1:
                    destination = entries
                sdIndex += 1
            if reg_hop.findall(entries):
                e2 = entries.split(',')
                total_hops += 1
                if e2[0] in dns_to_ip:
                    name_coverage += 1
                    report_line_entries.append(withDNS(e2[0]))
                else:
                    report_line_entries.append(withoutDNS(e2[0]))
            if sdIndex == 2 and hops == len(strs):
                if destination in dns_to_ip:
                    name_coverage += 1
                    report_line_entries.append(withDNS(destination))
                else:
                    report_line_entries.append(withoutDNS(destination))
                sdIndex += 1

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
    jsonFile = sys.argv[3]
    processFiles(dnsFile,trFile,jsonFile)
