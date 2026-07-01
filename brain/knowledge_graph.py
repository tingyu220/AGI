from brain.entity import Entity
from brain.relation import Relation


class KnowledgeGraph:

    def __init__(self):
        self.entities = {}
        self.relations = []

    def add_entity(self, name):

        if name not in self.entities:
            self.entities[name] = Entity(name)

        return self.entities[name]

    def add_relation(self, subject, predicate, obj):

        self.add_entity(subject)
        self.add_entity(obj)

        relation = Relation(
            subject,
            predicate,
            obj
        )

        self.relations.append(relation)

    def query(self, subject, predicate=None):

        results = []

        for relation in self.relations:

            if relation.subject == subject:

                if predicate is None:
                    results.append(relation)

                elif relation.predicate == predicate:
                    results.append(relation)

        return results

    def show(self):

        print("\n===== KNOWLEDGE GRAPH =====")

        for relation in self.relations:
            print(relation)

        print("===========================\n")