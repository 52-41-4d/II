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
