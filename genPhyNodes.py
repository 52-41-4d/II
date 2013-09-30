from pygeocoder import Geocoder

PHY_NODES = "/scratch/SIGCOMM14/Input/phyNodes.txt"
PHY_OUTPUT = "/scratch/SIGCOMM14/Output/phyNodes.txt"
outFile = open(PHY_OUTPUT,'w')

i = 0
with open(PHY_NODES,'r') as f:
    for line in f:
        i += 1
        try:
            (networkName, nodeName, address) = line.strip().replace('\"','').split('\t')
            results = Geocoder.geocode(address)
            outFile.write("%s=%s=%s=%s=%s\n" % (nodeName, networkName, address, results[0].city, results[0].country))
            if (i % 500 == 0):
                outFile.flush()
        except:
            continue

outFile.close() 
