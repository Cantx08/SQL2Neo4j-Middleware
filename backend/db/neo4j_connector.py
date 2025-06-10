from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234567890"))

def execute_cypher_query(query: str):
    with driver.session() as session:
        result = session.run(query)
        if "return" in query.lower():
            return [record.data() for record in result]
        else:
            summary = result.consume()
            count = summary.counters.nodes_created + summary.counters.nodes_deleted + summary.counters.properties_set
            return f"{count} nodos/relaciones afectados."
