from neo4j.v1 import GraphDatabase, basic_auth
#driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "cs1656"), encrypted=False)
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)
session = driver.session()

file = open("output.txt", "w")
file.write('### Q1 ###\n')
result = session.run("MATCH (m:Movie {title: 'Titanic'})<-[:ACTS_IN]-(a:Actor) RETURN a.name")
for record in result:
    file.write(("%s\n" %(record['a.name'])).encode('utf-8'))


file.write('### Q2 ###\n')

result = session.run("MATCH (d:Director)-[:DIRECTED]->(m:Movie) RETURN d.name, count(*) as cnt ORDER BY count(*) DESC LIMIT 100")
for record in result:
    file.write(("%s,%d\n" % (record['d.name'], record['cnt'])).encode('utf-8'))

file.write('### Q3 ###\n')

result = session.run("MATCH (m:Movie)<-[:ACTS_IN]-(a:Actor) RETURN m.title, count(*) as cnt ORDER BY count(*) DESC LIMIT 1")
for record in result:
    file.write(("%s,%d\n" % (record['m.title'], record['cnt'])).encode('utf-8'))

file.write('### Q4 ###\n')

result = session.run("MATCH (p:Person)-[:ACTS_IN]->(m:Movie)<-[:DIRECTED]-(d:Director) WITH p, count(distinct d.name) as cnt WHERE cnt >= 3 RETURN p.name, cnt")
for record in result:
    file.write(("%s,%d\n" % (record['p.name'], record['cnt'])).encode('utf-8'))

file.write('### Q5 ###\n')

result = session.run("match path = ((bacon:Actor {name: 'Kevin Bacon'})-[:ACTS_IN*4]-(costar:Actor)) WHERE NOT (bacon)-[:ACTS_IN]->()<-[:ACTS_IN]-(costar) RETURN DISTINCT costar.name as name;")
for record in result:
    file.write(("%s\n" % (record['name'])).encode('utf-8'))

####NEED TO DO 6 and 7!

file.write('### Q6 ###\n')

result = session.run("match path = ((bacon:Actor {name: 'Kevin Bacon'})-[:ACTS_IN*8]-(costar:Actor)) RETURN DISTINCT costar.name as name;")
for record in result:
    file.write(("%s\n" % (record['name'])).encode('utf-8'))

    #Q7 is commented out. It takes to long to run that it just crashed my computer. My idea behind it though was to get all bacon number paths period. 
    #Then after having all of them to get only those that are higher than 12 because that is what Professor Labrinidis said would 
    #qualify as being not included as a bacon number. 
file.write('### Q7 ###\n')
#result = session.run("match path = ((bacon:Actor {name: 'Kevin Bacon'})-[:ACTS_IN*]-(costar:Actor)) WHERE NOT (bacon)-[:ACTS_IN*24]-(costar) RETURN DISTINCT costar.name as name;")
#for record in result:
    #file.write(("%s\n" % (record['name'])).encode('utf-8'))

file.write('### Q8 ###\n')

result = session.run("MATCH ((a:Actor)-[:ACTS_IN]->(m:Movie)<-[:ACTS_IN]-(a2:Actor)) RETURN a.name as name, COUNT(distinct a2.name) as cnt ORDER BY cnt DESC LIMIT 50")
for record in result:
    file.write(("%s,%d\n" % (record['name'], record['cnt'])).encode('utf-8'))



session.close()
