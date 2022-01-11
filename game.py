import math
from constants import AI_TURN, COLUMN_COUNT, MINIMAX_DEPTH,PLAYER_TURN, ROW_COUNT, WINDOW_LENGTH
from ai import AI
import random

class Connect4:

	def __init__(self):
		self.grid=[[-1]*7 for i in range(6)]	
		self.turn = random.randint(PLAYER_TURN,AI_TURN)
		self.ai = AI()

	def isValid(self,row,col):
		return self.isValidCol(col) and self.isValidRow(row)

	def isValidCol(self,col):
		return (col > -1 and col < COLUMN_COUNT)
	
	def isValidRow(self,row):
		return (row > -1 and row < ROW_COUNT)
	
	def getValidLocations(self):
		validLocations = []
		for col in range(COLUMN_COUNT):
			row,isValid = self.getRow(col)
			if isValid:
				validLocations.append((row,col))
		return validLocations

	def getRow(self,col):
		if not self.isValidCol(col):
			return (-1,False)

		for i in range(5,-1,-1):
			if(self.grid[i][col] == -1):
				return (i,True)
		return (-1,False)

	def getTurnColor(self):
		color = 'red'
		if self.turn == AI_TURN:
			color = 'yellow'
		return color
	
	def getTurn(self):
		return self.turn

	def updateTurn(self):
		if self.turn == PLAYER_TURN:
			self.turn = AI_TURN
		else:
			self.turn = PLAYER_TURN

	def makeMove(self,row,col):
		self.grid[row][col] = self.turn
		return self.isWinningMove(row,col)
	
	def isWinningMove(self,row,col):
		horizontalCount = 0
		verticalCount = 0
		positiveDiagCount = 0
		negativeDiagCount = 0

		for j in range(1,WINDOW_LENGTH):
			if self.isValid(row,col+j) and self.grid[row][col+j] == self.turn:
				horizontalCount = horizontalCount+1
			else:
				break

		for j in range(1,WINDOW_LENGTH):	
			if self.isValid(row,col-j) and self.grid[row][col-j] == self.turn:
				horizontalCount = horizontalCount+1
			else:
				break

		if(horizontalCount >= 3 ):
			return True

		for j in range(1,WINDOW_LENGTH):		
			if self.isValid(row+j,col) and self.grid[row+j][col] == self.turn:
				verticalCount = verticalCount+1	
			else:
				break

		for j in range(1,WINDOW_LENGTH):
			if self.isValid(row-j,col) and self.grid[row-j][col] == self.turn:
				verticalCount = verticalCount+1	
			else:
				break
				
		if(verticalCount >= 3 ):
			return True
			
		for j in range(1,WINDOW_LENGTH):
			if self.isValid(row+j,col+j) and self.grid[row+j][col+j] == self.turn:
				positiveDiagCount = positiveDiagCount+1
			else:
				break
				
		for j in range(1,WINDOW_LENGTH):
			if self.isValid(row-j,col-j) and self.grid[row-j][col-j] == self.turn:
				positiveDiagCount = positiveDiagCount+1
			else:
				break

		if(positiveDiagCount >= 3 ):
			return True
			
		for j in range(1,WINDOW_LENGTH):
			if self.isValid(row-j,col+j) and self.grid[row-j][col+j] == self.turn:
				negativeDiagCount = negativeDiagCount+1
			else:
				break
				
		for j in range(1,WINDOW_LENGTH):
			if self.isValid(row+j,col-j) and self.grid[row+j][col-j] == self.turn:
				negativeDiagCount = negativeDiagCount+1
			else:
				break

		if(negativeDiagCount >= 3 ):
			return True

		return False

	def makeAIMove(self):
		move,score = self.ai.alphaBeta(self.grid,MINIMAX_DEPTH,-math.inf,math.inf,True)
		return move