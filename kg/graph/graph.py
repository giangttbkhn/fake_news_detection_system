from neo4j.v1 import GraphDatabase, BoltStatementResult
import traceback
from data.processor import DataProcessor, InputProcessor
import textdistance

URI = "bolt://localhost:7687"
USER_NAME = "neo4j"
PASS = "1234"


class Graph():
    def __init__(self):
        self.data_processor = DataProcessor()
        self.graphDB_Driver = GraphDatabase.driver(URI, auth=(USER_NAME, PASS), encrypted=False)

    def contribute_graph(self):
        if self.data_processor.sources == None:
            print("Please add source to contribute the graph")
        else:
            triples = self.data_processor.generate_triples()
            self._deploy_from_triples(triples)

    def checkExistNode(self, node):
        queryExistNode = "match (n:Entity{name:" + "'" + str(node.name) + "'" + " return count(n)"
        self._execute(queryExistNode)

    def delete_all_node(self):
        query = "match (n) detach delete (n)"
        self._execute(query)

    def detect_fake_news(self, sentence):
        self.data_processor.news = sentence
        self.data_processor.analyse_input()
        if len(self.data_processor.triples) == 0:
            print("Please type another news, we can not extract information from previous news\n")
        for t in self.data_processor.triples:
            result = self._has_information(t)
            self._respone_true(t) if result.value()[0] != 0 else self._response_false(t)

    #=====================================================================================================
    #                                            Internal function
    #=====================================================================================================

    def _execute(self, query):
        with self.graphDB_Driver.session() as graphDB_Session:
            return graphDB_Session.run(query)

    def _deploy_from_triples(self, triples):
        try:
            for triple in triples:
                head = triple.head
                relation = triple.relation
                tail = triple.tail
                query = "merge (head:Entity" + "{name:" + "'" + str(head.name) + "'" + "})" \
                        + "merge (tail:Entity" + "{name:" + "'" + str(tail.name) + "'" + "})" \
                        + "merge (head)-[:" + str(relation.label) + "{name:" + "'" + str(
                    relation.name) + "'" + "}]" + "->(tail)"
                self._execute(query)
        except:
            traceback.print_exc()

    def _has_information(self, triple):
        query = "match (n:Entity {name:" + "'" + str(triple.head.name) + "'})-[r]->(m:Entity {name:" \
                + "'" + str(triple.tail.name) + "'}) where r.name = " + "'" \
                + str(triple.relation.name) + "'" + " return count(r)"
        return self._execute(query)

    def _respone_true(self,triple):
        print("Answer:This news is true\n")
        print("Triple extracted: " + str(triple.head.name) + " " + str(triple.relation.name) + " " + str(
            triple.tail.name) + "\n")
        print("===============================================================\n")

    def _response_false(self, triple):
        qRelation = "match (n:Entity {name:" + "'" + str(triple.head.name) + "'})-[r]->(m:Entity) return r.name, m.name"
        results = self._execute(qRelation)
        dictRelationScore = {}
        dictRelationEntity = {}
        for r in results.values("r.name", "m.name"):
            dictRelationEntity[r[0]] = r[1]
            score = textdistance.jaro_winkler(triple.relation.name, r[0])
            dictRelationScore[r[0]] = score

        if len(dictRelationScore) == 0:
            print("Answer: We do not have this news\n")
            print("Triple extracted: " + str(triple.head.name) + " " + str(triple.relation.name) + " " + str(
                triple.tail.name) + "\n")
            print("===============================================================\n")
        else:
            print("Answer: We do not have this news, may be you want to know st:\n")
            print("Triple extracted: " + str(triple.head.name) + " " + str(triple.relation.name) + " " + str(triple.tail.name) + "\n")

            dictRelationScore = {k: v for k, v in
                                 sorted(dictRelationScore.items(), key=lambda item: item[1], reverse=True)}
            count = 0
            for r, s in dictRelationScore.items():
                print(">>> " + str(triple.head.name) + " " + str(r) + " " + str(dictRelationEntity.get(r)))
                print("relation has similarity: ", s)
                print("\n")
                count = count + 1
                if count == 3:
                    break
            print("===============================================================\n")

if __name__ == "__main__":
    graph = Graph()
    graph.detect_fake_news("hi")
