import sys
import time
import enum
import random

class Direction(enum.Enum):
  Up = 0
  Down = 1
  Left = 2
  Right = 3

def Factorial(n):
  factorial = 1
  if int(n) >= 1:
    for i in range (1,int(n)+1):
      factorial = factorial * i
  return factorial

def listToString(list):
  str1 = ""
  return (str1.join(list))

def printList(list):
  str = ""
  for i in range(len(list)):
    if ((i - 4) % 4 == 0): 
      print(str)
      str = ""
    str += list[i]
  print(str)

def GetHammingDistance(string1, string2):
  return sum(c1 != c2 for c1, c2 in zip(string1, string2))

targetTiles = "123456789ABCDEF "

class Board:


  Tiles = ""
  Cost = 0 # g cost - initialized in GetPossibleBoards()
  MisplacedTiles = 0 # h cost
  def CostMisplacedTiles(board):
    return board.Cost + board.MisplacedTiles # f cost

  Parent = None

  def __init__(self, tiles):
    if (tiles == ""):
      self.Tiles = targetTiles
    else:
      self.Tiles = tiles

  @staticmethod
  def SolveWithAStar(start, finish):
    print("Starting board")
    
    printList(start.Tiles)
    print()
    print("Target board")
    printList(finish.Tiles)
    print()

    start.SetMisplacedTiles(finish)

    activeBoards = [start]
    visitedBoards = []

    print("Searching...\n")
    boardLimit = Factorial(len(start.Tiles)) / 2
    iterations = 0
    runtime = time.time()
    while (len(activeBoards) > 0):
      # retrieve the board with the lowest f cost
      activeBoards.sort(key = lambda x: x.CostMisplacedTiles())
      checkBoard = activeBoards[0]

      iterations += 1
      if (iterations >= boardLimit):
        print("Iteration limit reached! No Path Found!")
        return

      if (checkBoard.MisplacedTiles == 0):
        print("Solution found!")
        print("Optimal moveset:\n")
        optimalMoveset = []
        # Find optimal moveset
        while (checkBoard.Parent != None):
          optimalMoveset.append(checkBoard)
          checkBoard = checkBoard.Parent
        # Print optimal moves
        counter = 0
        print("Start")
        printList(start.Tiles)
        print()
        for i in range(len(optimalMoveset)-1, -1, -1):
          board = optimalMoveset[i]
          counter += 1
          print("Move " + str(counter))
          printList(board.Tiles)
          print()
        #
        print("Runtime: " + str(time.time()- runtime) + " ms")
        if (len(sys.argv) > 1):
          print("Number of scrambles: " + sys.argv[1])
        else:
          print("Number of scrambles: 10")
        print("Number of moves: " + str(len(optimalMoveset)))
        print("Visited Boards: " + str(len(visitedBoards)))
        print("Active Boards: " + str(len(activeBoards)))
        visitedMemory = sys.getsizeof(visitedBoards)
        print("Visited Boards Memory: " + str(visitedMemory) + " bytes")
        activeMemory = sys.getsizeof(activeBoards)
        print("Active Boards Memory: " + str(sys.getsizeof(activeBoards)) + " bytes")
        print("Cummulative Memory: " + str(visitedMemory + activeMemory) + " bytes")
        return

      visitedBoards.append(checkBoard)
      activeBoards.remove(checkBoard)

      # print('\033[1;1H')
      # print("Visited Boards: " + visitedBoards.count())
      # print("Active Boards: " + activeBoards.count())
      # print("Solution limit: " + visitedBoards.count() + " / " + boardLimit + " = " + (visitedBoards.count()/boardLimit) + "%")

      possibleBoards = Board.GetPossibleBoards(checkBoard, finish)

      for possibleBoard in possibleBoards:
        if (Board.ListHasBoard(visitedBoards, possibleBoard)):
          continue

        if (Board.ListHasBoard(activeBoards, possibleBoard)):
          existingBoard = Board.ListFirstBoard(activeBoards, possibleBoard)
          if (existingBoard.CostMisplacedTiles() > checkBoard.CostMisplacedTiles()):
            activeBoards.remove(existingBoard)
            activeBoards.append(possibleBoard)
        else:
          activeBoards.append(possibleBoard)
    print("No Path Found!")

  def ListHasBoard(list, target):
    for i in range(len(list)):
      if list[i].Tiles == target.Tiles:
        return True
    return False

  def ListFirstBoard(list, target):
    for i in range(len(list)):
      if list[i].Tiles == target.Tiles:
        return list[i]
    return None

  # Hamming distance between this board and our target board
  def SetMisplacedTiles(self, target):
    self.MisplacedTiles = GetHammingDistance(self.Tiles, target.Tiles)

  @staticmethod
  def GetPossibleBoards(currentBoard, targetBoard):
    possibleBoards = []

    # add to possibleBoards
    board = Board(Board.MoveTile(currentBoard, Direction.Up))
    board.Parent = currentBoard
    board.Cost = currentBoard.Cost + 1
    possibleBoards.append(board)
    board = Board(Board.MoveTile(currentBoard, Direction.Down))
    board.Parent = currentBoard
    board.Cost = currentBoard.Cost + 1
    possibleBoards.append(board)
    board = Board(Board.MoveTile(currentBoard, Direction.Left))
    board.Parent = currentBoard
    board.Cost = currentBoard.Cost + 1
    possibleBoards.append(board)
    board = Board(Board.MoveTile(currentBoard, Direction.Right))
    board.Parent = currentBoard
    board.Cost = currentBoard.Cost + 1
    possibleBoards.append(board)

    for possibleBoard in possibleBoards:
      possibleBoard.SetMisplacedTiles(targetBoard)

    return possibleBoards
  
  @staticmethod
  def MoveTile(board, direction):
    newTiles = list(board.Tiles)
    index = board.Tiles.index(' ')
    newIndex = index
    if (Direction(direction) == Direction.Up):
      if (index > 4): newIndex = index - 4 # 4 is total number of rows in our puzzle
    elif (Direction(direction) == Direction.Down):
      if (index < 16 - 4): newIndex = index + 4 # 4 is total number of rows in our puzzle
    elif (Direction(direction) == Direction.Left):
      if (index % 4 != 0): newIndex = index - 1
    elif (Direction(direction) == Direction.Right):
      if ((index - 3) % 4 != 0): newIndex = index + 1
    # Move the tile
    newTiles[index] = newTiles[newIndex]
    # Set the tiles old position to ' '
    newTiles[newIndex] = ' '
    newTiles = listToString(newTiles)
    return newTiles

  @staticmethod
  def RandomBoard(numberOfMoves):
    board = Board("")
    for i in range(numberOfMoves):
      board.Tiles = Board.MoveTile(board, random.randint(0, 3))
    return board

print("================================================")
print("Homework 3 - A* with 15 puzzle problem")
print("Heuristic used is # of misplaced tiles, counted with Hamming distance")
print("================================================")
if (len(sys.argv) > 1):
  start = Board.RandomBoard(int(sys.argv[1]))
else:
  start = Board.RandomBoard(10)
#printList(start.Tiles)
finish = Board("")
#printList(finish.Tiles)
Board.SolveWithAStar(start, finish)