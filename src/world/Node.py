from src.world.Connection import Connection
from src.Constants import *

class Node:
    def __init__(self, rowRange:range, col:int, nodeID:int):
        self.row1 = rowRange[0]
        self.row2 = rowRange[-1]
        self.col = col
        self.nodeID = nodeID
        self.connections: list[Connection] = []
        self.entryInterval = rowRange if col == 0 else range(0, 0)
        self.resetConnections()

    def connect(self, target:'Node', exitInterval:range):
        self.connections.append(Connection(target, exitInterval))
        target.isOrphaned = False
        target.entryInterval = exitInterval

    def connectionInterval(self, target:'Node') -> int:
        for connection in self.connections:
            if connection.target == target:
                return connection.getIntervalDistance(self.entryInterval)
        return -1

    def resetConnections(self):
        self.connections = []
        if self.col != 0:
            self.isOrphaned = True
        else:
            self.isOrphaned = False