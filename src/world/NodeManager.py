from src.world.Node import Node
from src.Constants import *
import random
from typing import List

class NodeManager:
    

    def __init__(self, mapRows:int, mapCols:int):
        self.mapRows = mapRows
        self.mapCols = mapCols
        self.nodeList: List[Node] = []
        self.currentNodeID = 0
        self.currentPath: List[Node] = []
        for i in range(self.mapCols - 1):
            self.addNode(range(1, mapRows-1), i)
        self.doorNode = self.getNodeByID(self.addNode(range(7, 8), self.mapCols - 1))   # Final node at the door (row 7)
        self.nodeConnectionLoop()

    def addNode(self, range:range, col:int) -> int:
        newNode = Node(range, col, self.currentNodeID)
        self.nodeList.append(newNode)
        self.currentNodeID += 1
        return self.currentNodeID - 1

    def removeNode(self, node:Node):
        self.nodeList.remove(node) 

    def removeAllConnections(self):
        for node in self.nodeList:
            node.resetConnections()     # All nodes become orphans except for the root nodes (col == 0)

    def updateConnection(self, directionStr:str) -> bool:
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
                    if (intersect := range(max(nextNode.row1, node.row1), min(nextNode.row2, node.row2)+1)) and \
                        node.connectionInterval(nextNode) == -1 and nextNode.connectionInterval(node) == -1: # Checks if two number ranges intersect
                        newConnection = True
                        node.connect(nextNode, intersect)
        return newConnection


    def pathFind(self, node:Node, path: list[Node], totalLength=0) -> tuple[list[Node], bool, int]:         # Recursion fun
        path = path.copy()
        path.append(node)
        shortestPath: List[Node] = []
        shortestLength: int = 999
        if (distance := node.connectionInterval(self.doorNode)) != -1:
            pathFound = True
            shortestPath.append(self.doorNode)
            shortestPath.append(node)            
            shortestLength = totalLength + 1    # For moving one column normally
            shortestLength += distance
        elif not node.connections:          # Dead end
            pathFound = False
        else:                     
            for connection in node.connections:
                connectionLength = totalLength + 1    # For moving one column normally
                connectionLength += node.connectionInterval(connection.target)
                results = self.pathFind(connection.target, path, connectionLength)
                if results[1] and results[2] < shortestLength:
                    pathFound = True
                    shortestPath = results[0]
                    shortestPath.append(node)
                    shortestLength = results[2]
                    break
            else:
                pathFound = False
        return (shortestPath, pathFound, shortestLength)

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
            self.currentPath = []
                
            
    def addBlock(self, row:int, col:int) -> bool:   # Splits the node the block (tower/blockade) is on into two nodes
        for node in self.getNodesByColumn(col):
            if row in range(node.row1, node.row2+1):
                temp = (node.row1, node.row2)
                topNode = None
                bottomNode = None
                if node.row1 < row:
                    topNode = self.addNode(range(node.row1, row), col)
                if row < node.row2:
                    bottomNode = self.addNode(range(row + 1, node.row2+1), col)
                self.removeNode(node)
                self.removeAllConnections()
                self.nodeConnectionLoop()

                print("printing ALL nodes")
                for node2 in self.nodeList:
                    print((node2.col, node2.row1, node2.row2))

                if self.currentPath == []:
                    if topNode is not None:
                        self.removeNode(self.getNodeByID(topNode))
                    if bottomNode is not None:
                        self.removeNode(self.getNodeByID(bottomNode))
                    self.addNode(range(temp[0], temp[1]+1), col)
                    self.removeAllConnections()
                    self.nodeConnectionLoop()
                    return False
        
        return True     # Good enough for now?

    def getNodesByColumn(self, col:int) -> list[Node]:
        return [node for node in self.nodeList if node.col == col]
    
    def getNodeByID(self, nodeID:int) -> Node:
        return [node for node in self.nodeList if node.nodeID == nodeID][0]
