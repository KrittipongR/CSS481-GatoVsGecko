from src.world.Node import Node
from src.Constants import *
import random
from typing import List
import pygame

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
        self.blocks = []

    def addNode(self, rowRange:range, col:int) -> int:
        newNode = Node(rowRange, col, self.currentNodeID)
        self.nodeList.append(newNode)
        self.currentNodeID += 1
        return self.currentNodeID - 1
    
    # def verifyColumn(self, col:int):   # Vertically adjacent nodes get merged
    #     nodes = self.getNodesByColumn(col)
    #     for node1 in nodes:
    #         for node2 in nodes:
    #             if node1.row2 == node2.row1 - 1:
    #                 self.addNode(range(node1.row1, node2.row2 + 1), col)

    def removeBlock(self, grid: tuple[int, int]):
        print("BLOCKS")
        print(self.blocks)
        for block in self.blocks:
            if block == grid:
                self.blocks.remove(block)
                self.refreshColumn(grid[1])
                break

    def refreshColumn(self, col:int):
        for node in self.getNodesByColumn(col):
            print("NODE REMOVED:")
            print((node.col, node.row1, node.row2))
            print("---------------")
            self.removeNode(node)

        blockRows = [block[0] for block in self.blocks if block[1] == col]
        blockRows = [0] + sorted(blockRows) + [self.mapRows - 1]

        for i in range(len(blockRows) - 1):
            rowRange = range(blockRows[i] + 1, blockRows[i+1])
            if rowRange:    # If gap, car
                
                self.addNode(rowRange, col)



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
                
            
    def addBlock(self, row:int, col:int, validateOnly:bool = False) -> bool:   # Splits the node the block (tower/blockade) is on into two nodes
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
                if not validateOnly:
                    print("printing ALL nodes")
                    for node2 in self.nodeList:
                        print((node2.col, node2.row1, node2.row2))

                if self.currentPath == [] or validateOnly:
                    if topNode is not None:
                        self.removeNode(self.getNodeByID(topNode))
                    if bottomNode is not None:
                        self.removeNode(self.getNodeByID(bottomNode))
                    self.addNode(range(temp[0], temp[1]+1), col)
                    self.removeAllConnections()
                    self.nodeConnectionLoop()
                    return False or validateOnly
        
        self.blocks.append((row, col))
        return True     # Good enough for now?

    def getNodesByColumn(self, col:int) -> list[Node]:
        return [node for node in self.nodeList if node.col == col]
    
    def getNodeByID(self, nodeID:int) -> Node:
        return [node for node in self.nodeList if node.nodeID == nodeID][0]
    
    # def renderPath(self, screen: pygame.Surface):
    #     """ Render the current path for the gecko on the screen. """
    #     # Path color (Red for the path)
    #     path_color = (255, 0, 0)  # Red color for the path
    #     waypoint_color = (0, 255, 0)  # Green color for waypoints

    #     # Loop through the currentPath to draw lines between consecutive nodes
    #     for i in range(len(self.currentPath) - 1):
    #         start_node = self.currentPath[i]
    #         end_node = self.currentPath[i + 1]

    #         # Convert node positions to screen coordinates
    #         # Start at top-left of the node, adjust for tile center if needed
    #         start_pos = (start_node.col * TILE_SIZE + TILE_SIZE // 2, start_node.row1 * TILE_SIZE + TILE_SIZE // 2)
    #         end_pos = (end_node.col * TILE_SIZE + TILE_SIZE // 2, end_node.row1 * TILE_SIZE + TILE_SIZE // 2)

    #         # Draw a line between consecutive nodes in the path
    #         pygame.draw.line(screen, path_color, start_pos, end_pos, 3)  # Line thickness is 3

    #         # Optionally, draw circles at each waypoint to indicate the nodes
    #         pygame.draw.circle(screen, waypoint_color, start_pos, 5)  # Small circles for waypoints
    #         pygame.draw.circle(screen, waypoint_color, end_pos, 5)  # Small circles for waypoints

