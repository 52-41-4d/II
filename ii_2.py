## TODO
## Higher level:
## Add physical information - Internet Atlas
## Add peering information - PeeringDB
## Add asn information - RouteViews
## Eat file from PhaseOne and apply other information from Neo4j lookups using Gremlin/Bulb framework
##
## Algorithm:
## for every TR:
##     search the info in neo4j for candidates using Gremlin queries
##     found? Good
##     Not found? Suggest Phase three targetted probing

from bulbs.neo4jserver import Graph

if __name__=="__main__":
    # Write code to read the file from phase one

    # Graph initialization code
    g = Graph()
    g.scripts.update('GremlinQuery/gremlin.groovy')
    script = g.scripts.get('rank_items')
    params = dict(user_id=3)
    items = g.gremlin.query(script, params)
