import redis

def FlushAndInsert(r):
    r.flushall()
    r.set('127.0.0.1','1')
    r.set('127.0.0.2','2')
    r.set('127.0.0.3','3')
    r.set('127.0.0.4','4')
    r.set('127.0.0.5','5')
    r.set('127.0.0.6','6')
    r.set('127.0.0.7','7')
    r.set('127.0.0.8','8')
    r.set('127.0.0.9','9')
    r.set('127.0.0.10','10')
   
def RedisPipeline(r,ipList):
    pipe = r.pipeline()
    for ip in ipList:
        pipe.get(ip)
    values = pipe.execute()
    return values

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    FlushAndInsert(r)
    print "Data inserted"

    ipList = []
    ipList.append('127.0.0.1') 
    ipList.append('127.0.0.2') 
    ipList.append('127.0.0.3') 
    ipList.append('127.0.0.4') 
    ipList.append('127.0.0.5') 
    ipList.append('127.0.0.6') 
    ipList.append('127.0.0.7') 
    ipList.append('127.0.0.8') 
    ipList.append('127.0.0.9') 
    ipList.append('127.0.0.10') 
    ipList.append('127.0.0.11') 

    print "IP list created"
    values = RedisPipeline(r,ipList)  
    print values
