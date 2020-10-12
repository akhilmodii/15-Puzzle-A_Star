import os
import time


import itertools

import psutil


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.middle1 = None
        self.middle2 = None
        self.data = value
        self.parent = None




class Tree:
    def createNode(self, data):
        return Node(data)

    def insert(self, node, data):
        """
        Insert function will insert a node into tree.
        Duplicate keys are not allowed.
        """
        # if tree is empty , return a root node
        if node is None:
            return self.createNode(data)
        # if data is smaller than parent , insert it into left side
        if node.data == data:
            return node
        elif node.left == None:
            node.left = self.insert(node.left, data)
        elif node.right == None:
            node.right = self.insert(node.right, data)
        elif node.middle1 == None:
            node.middle1 = self.insert(node.middle1, data)
        else:
            node.middle2 = self.insert(node.middle2, data)

        return node


# Method tp check if two lists are equal.
def checkEQ(list1, list2):
    if list1 == list2:
        return True
    else:
        return False


movesList = []  # Empty List. Will contain all the moves made to reach the solution.


# Method to evaluate moves made.
def moves(input):
    list = []
    boardList = eval(input)
    x = 0
    while 0 not in boardList[x]:
        x = x + 1
    y = boardList[x].index(0)

    if x > 0:  # Shifting UP
        boardList[x][y], boardList[x - 1][y] = boardList[x - 1][y], boardList[x][y]
        list.append(str(boardList))
        movesList.append('U')
        # moveValue = 'U'
        boardList[x][y], boardList[x - 1][y] = boardList[x - 1][y], boardList[x][y]

    if x < 3:  # Shifting DOWN
        boardList[x][y], boardList[x + 1][y] = boardList[x + 1][y], boardList[x][y]
        list.append(str(boardList))
        movesList.append('D')
        # moveValue = 'D'
        boardList[x][y], boardList[x + 1][y] = boardList[x + 1][y], boardList[x][y]

    if y > 0:  # Shifting LEFT
        boardList[x][y], boardList[x][y - 1] = boardList[x][y - 1], boardList[x][y]
        list.append(str(boardList))
        movesList.append('L')
        # moveValue = 'L'
        boardList[x][y], boardList[x][y - 1] = boardList[x][y - 1], boardList[x][y]

    if y < 3:  # Shifting RIGHT
        boardList[x][y], boardList[x][y + 1] = boardList[x][y + 1], boardList[x][y]
        list.append(str(boardList))
        movesList.append('R')
        # moveValue = 'R'
        boardList[x][y], boardList[x][y + 1] = boardList[x][y + 1], boardList[x][y]

    return list


def misplacedTiles(initialBoard):
    """
    :param initialBoard:
    :return: numMisplacedTiles
    This function is an implementation of the heuristic which counts the number of misplaced tiles.
    """
    numMisplacedTiles = 0
    compare = 0
    board = eval(initialBoard)
    for i in range(0, 4):
        for j in range(0, 4):
            if board[i][j] != compare:
                numMisplacedTiles = numMisplacedTiles + 1
            compare = compare + 1
    return numMisplacedTiles


def manhattanDistance(initialBoard):
    """
    :param initialBoard:
    :return: distance
    This function is the implementation of the heuristic which implements the calculation of manhattan distance
    between the tiles.
    """
    distance = 0
    board = eval(initialBoard)
    for i in range(0, 4):
        for j in range(0, 4):
            if board[i][j] == 0:
                continue
            distance = distance + abs(i - board[i][j]/4) + abs(j - board[i][j]%4)
    return distance



def astarManhattan(initialBoard, finalBoard):
    """
    :param initialBoard:
    :param finalBoard:
    This function implements the A-star algorithm using the Manhattan Distance Heuristic.
    """

    print('============================================================================================')
    print('\t\t\t\t\tSolution Using Manhattan Distance Heuristic')
    print('============================================================================================')
    front = [[manhattanDistance(initialBoard), initialBoard]]
    expandedNodes = []
    while front:
        i=0
        for j in range(1, len(front)):
            if front[i][0] > front[j][0]:
                i=j
        path = front[i]
        front = front[:i] + front[i+1:]
        endNode = path[-1]
        if endNode == finalBoard:
            break
        for move in moves(endNode):
            newPath = [path[0] + manhattanDistance(move) - manhattanDistance(endNode)] + path[1:] + [move]
            expandedNodes.append(endNode)
    print('Expanded Nodes: ' + str(len(expandedNodes)))
    print('Solution: ')
    printMoves(movesList)



def astarMisplaced(initialBoard, finalBoard):
    """
    :param initialBoard:
    :param finalBoard:
    This function implements the A-star algorithm using the Misplaced Tiles Heuristic.
    """

    print('============================================================================================')
    print('\t\t\t\t\tSolution Using Misplaced Tiles Heuristic')
    print('============================================================================================')
    front = [[misplacedTiles(initialBoard), initialBoard]]
    expandedNodes = []
    while front:
        i=0
        for j in range(1, len(front)):
            if front[i][0] > front[j][0]:
                i=j
        path = front[i]
        front = front[:i] + front[i+1:]
        endNode = path[-1]
        if endNode == finalBoard:
            break
        for move in moves(endNode):
            newPath = [path[0] + misplacedTiles(move) - misplacedTiles(endNode)] + path[1:] + [move]
            expandedNodes.append(endNode)
    print('Expanded Nodes: ' + str(len(expandedNodes)))
    print('Solution: ')
    printMoves(movesList)



# Formats the user input.
def inputFormat(userInput):
    newList = []
    userInput = userInput.replace(" ", ",")
    newUserInput = [str(k) for k in userInput.split(',')]
    newUserInput = list(map(int, newUserInput))
    for i in range(0, len(newUserInput), 4):
        newList.append(newUserInput[i:i + 4])
    return newList


# printing all the moves made to reach the solution.
def printMoves(list):
    for i in range(len(list)):
        print(list[i], end="")
    print('\n')


if __name__ == "__main__":
    userInput = input("Enter initial configuration: ")
    startTime = time.time()
    process = psutil.Process(os.getpid())
    initialMemory = process.memory_info().rss / 1024.0
    newList = inputFormat(userInput)
    initialBoard = str(newList)
    finalBoard = str([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    input1 = input('Please enter heuristic you want to use. Enter 1 for Manhattan Heuristic or 2 for Misplaced Tile heuristic: ')
    if input1 == '1':
        astarManhattan(initialBoard, finalBoard)
    elif input1 == '2':
        astarMisplaced(initialBoard, finalBoard)
    else:
        print('Wrong Input')
    finalMemory = process.memory_info().rss / 1024.0
    totalMemory = finalMemory - initialMemory
    endTime = time.time()
    totalTime = endTime - startTime
    print('Time taken: ' + str(totalTime))
    print('Total Memory used: ' + str(finalMemory) + ' KB')

"""
Inputs: 
1 0 3 4 5 2 6 8 9 10 7 11 13 14 15 12   

1 2 3 4 5 6 8 0 9 11 7 12 13 10 14 15

1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15

1 2 0 4 6 7 3 8 5 9 10 12 13 14 11 15 

1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12

"""
