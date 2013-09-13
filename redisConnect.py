import redis
import sys

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.flushall()
    i = 0
    with open(sys.argv[1],'r') as ip_to_asn:
        for line in ip_to_asn:
            l = line.rstrip().split("|")
            key=l[1].strip()
            value=l[0].strip()
            r.set(key,value)
            print "%s,%s" % (key,value)
            i += 1
            if ( i % 10000 == 0):
                print "************** i = %s" % (i)
