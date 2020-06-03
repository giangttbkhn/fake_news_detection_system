
class Entity:
    def __init__(self, name=""):
        self.name = name
        self.label = 'Entity'

class Relation:
    def __init__(self, name="", label = ""):
        self.name = name
        self.label = label if label != '' else 'relation'

class Triple:
    def __init__(self,head, relation, tail):
        self.head = head
        self.relation = relation
        self.tail = tail