class Node:
    def __init__(self, state):
        self.state = state
        self.weight = 0
        self.parent = None
        self.children = []
    
    def SetWeight(self, weight):
        self.weight = weight

    def AppendChild(self, child):
        self.children.append(child)
        child.parent = self