PHY_LINKS = "/scratch/SIGCOMM14/Input/phyLinks.txt"

i = 0
with open(PHY_LINKS,'r') as f:
    for line in f:
        i += 1
        try:
            (nodeA, nodeB) = line.strip().replace('\"','').split('\t')
            print "%s,%s" % (nodeA, nodeB)
        except:
            continue
