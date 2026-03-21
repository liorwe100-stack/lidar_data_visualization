import math
class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, pos=None,g = None, parent: 'Node' = None):
        self.pos = pos
        self.parent = parent
        if g is not None:
            self.g = g
        else:
            self.g = 0
        self.h = 0
        self.f = 0
    def __lt__(self, other):
        return (self.f,self.h) < (other.f, other.h)
    def __eq__(self, other):
        return self.pos == other.pos
    def setG(self, g):
        self.g = g
    def setH(self,end_node: 'Node'):
        self.h = math.dist(self.pos,end_node.pos)
        self.f = self.g + self.h
    def setParent(self,parent):
        self.parent = parent