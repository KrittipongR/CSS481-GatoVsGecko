from src.world.Node import Node
from src.Constants import *
import random

class NodeManager:
    

    def __init__(self, mapRows, mapCols):
        self.mapRows = mapRows
        self.mapCols = mapCols
        self.nodeList = []
        self.currentNodeID = 0
        self.currentPath = []
        for i in range(self.mapCols - 1):
            self.addNode(row1=0, row2=mapRows-1, col=i)
        self.nodeConnectionLoop()
        pass

    def addNode(self, row1, row2, col):
        newNode = Node(row1=row1, row2=row2, col=col, nodeID=self.currentNodeID)
        self.nodeList.append(newNode)
        self.currentNodeID += 1
        return self.currentNodeID - 1

    def removeNode(self, node):
        self.nodeList.remove(node) 

    def removeAllConnections(self):
        for node in self.nodeList:
            node.resetConnections()     # All nodes become orphans except for the root nodes (col == 0)

    def updateConnection(self, directionStr):
        directions = {
            "left": -1,
            "right": 1
        }
        direction = directions[directionStr]
        newConnection = False
        self.nodeList = sorted(self.nodeList, key=lambda x: x.col)  # Sort by column, ascending
        for node in self.nodeList:            
            if not node.isOrphaned:     # Only non-orphans can make a connection
                for nextNode in self.getNodesByColumn(node.col+direction):
                    if range(max(nextNode.row1, node.row1), min(nextNode.row2, node.row2)+1) and nextNode not in node.connections and node not in nextNode.connections: # Checks if two number ranges intersect
                        newConnection = True
                        node.connect(nextNode)
        return newConnection

    def pathFind(self, node, path):         # Recursion fun
        path = path.copy()
        path.append(node)
        if node.col == self.mapCols - 2 and 7 in range(node.row1, node.row2 + 1):   # Reach the door (row 7)
            pathFound = True
        elif not node.connections:          # Dead end
            print("dead end:" + str((node.col, node.row1, node.row2)))
            pathFound = False
        else:
            for nextNode in node.connections:            
                results = self.pathFind(nextNode, path)
                if results[1]:
                    pathFound = True
                    path = results[0]
                    break
            else:
                pathFound = False
        return (path, pathFound)

    def nodeConnectionLoop(self):
        roots = [node for node in self.nodeList if node.col == 0]
        random.shuffle(roots)               # Why not
        for root in roots:                  # This loop is cursed, sorry
            while not (pathResult := self.pathFind(root, []))[1]:
                if not (self.updateConnection("right") or self.updateConnection("left")): # No new connections either way and still no path
                    break
            else:   # Path is found
                self.currentPath = pathResult[0]
                break
        else:
            print("-- No path found, the algorithm has halted --")
            print("Falling back to previous path.")
            self.currentPath = None
                
            
    def addBlock(self, row, col):   # Splits the node the block (tower/blockade) is on into two nodes
        for node in self.getNodesByColumn(col):
            if row in range(node.row1, node.row2+1):
                temp = (node.row1, node.row2)
                topNode = None
                bottomNode = None
                if node.row1 < row:
                    topNode = self.addNode(node.row1, row-1, col)
                if row < node.row2:
                    bottomNode = self.addNode(row + 1, node.row2, col)
                self.removeNode(node)
                self.removeAllConnections()
                self.nodeConnectionLoop()
                if self.currentPath is None:
                    if topNode is not None:
                        self.removeNode(self.getNodeByID(topNode))
                    if bottomNode is not None:
                        self.removeNode(self.getNodeByID(bottomNode))
                    self.addNode(temp[0], temp[1], col)
                    self.removeAllConnections()
                    self.nodeConnectionLoop()
                    return False
        
        return True     # Good enough for now?

    def getNodesByColumn(self, col):
        return [node for node in self.nodeList if node.col == col]
    
    def getNodeByID(self, nodeID):
        return [node for node in self.nodeList if node.nodeID == nodeID][0]
