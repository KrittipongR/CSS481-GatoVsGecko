class Node:
    def __init__(self, row1, row2, col, nodeID):
        self.row1 = row1
        self.row2 = row2
        self.col = col
        self.nodeID = nodeID
        self.resetConnections()

    def connect(self, node):
        self.connections.append(node)
        node.isOrphaned = False

    def resetConnections(self):
        self.connections = []
        if self.col != 0:
            self.isOrphaned = True
        else:
            self.isOrphaned = False