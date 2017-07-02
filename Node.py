class Node:
    def __init__(self, state):
        self.state = state
        self.wins = 0.0
        self.visits = 0.0
        self.ressq = 0.0
        self.parent = None
        self.children = []
        self.sputc = 0.0
    
    def SetWeight(self, weight):
        self.weight = weight

    def AppendChild(self, child):
        self.children.append(child)
        child.parent = self

    def IsEqual(self, Node):
        if(self.state == Node.state):
            return True
        else:
            return False