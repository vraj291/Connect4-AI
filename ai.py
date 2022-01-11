import math
import random
from constants import AI_TURN,COLUMN_COUNT, EMPTY, NEGATIVE_POSITION_SCORES, PLAYER_TURN, POSITIVE_POSITION_SCORES, ROW_COUNT, WINDOW_LENGTH
import copy

class AI:

	def __init__(self):
		pass

	def makeMove(self,grid,validLocations):
		bestScore = -100
		bestMove = (-1,-1)
		for row,col in validLocations:
			tempGrid = copy.deepcopy(grid)
			tempGrid[row][col] = AI_TURN
			score = self.getPostionScore(tempGrid)
			if(score > bestScore):
				bestScore = score
				bestMove = (row,col)
		return bestMove

	def getWindowScore(self,window):
		diskCount = window.count(AI_TURN)
		oppCount = window.count(PLAYER_TURN)
		emptyCount = window.count(EMPTY)
		score = 0
		if diskCount == 4 or (diskCount == 3 and emptyCount == 1) or (diskCount == 2 and emptyCount == 2):
			score = score + POSITIVE_POSITION_SCORES[diskCount-1]
		if oppCount == 3 and emptyCount == 1:
			score = score + NEGATIVE_POSITION_SCORES[oppCount-1]
		return score

	def getPostionScore(self,grid):
		score = 0

		for i in range(ROW_COUNT):
			row = grid[i]
			for j in range(COLUMN_COUNT-WINDOW_LENGTH+1):
				score = score + self.getWindowScore(row[j:j+WINDOW_LENGTH])

		for i in range(COLUMN_COUNT):
			col = [grid[j][i] for j in range(ROW_COUNT)]
			for j in range(ROW_COUNT-WINDOW_LENGTH+1):
				score = score + self.getWindowScore(col[j:j+WINDOW_LENGTH])
		
		for i in range(ROW_COUNT-WINDOW_LENGTH+1):
			for j in range(COLUMN_COUNT-WINDOW_LENGTH+1):
				window = [grid[i+WINDOW_LENGTH-1-c][j+c] for c in range(WINDOW_LENGTH)]
				score = score + self.getWindowScore(window)

		for i in range(ROW_COUNT-WINDOW_LENGTH+1):
			for j in range(COLUMN_COUNT-WINDOW_LENGTH+1):
				window = [grid[i+c][j+c] for c in range(WINDOW_LENGTH)]
				score = score + self.getWindowScore(window)

		return score

	def isTerminalNode(self,grid):
		if (self.isGameOver(grid,AI_TURN)):
			return math.inf
		elif (self.isGameOver(grid,PLAYER_TURN)):
			return -math.inf
		elif (len(self.getValidLocations(grid)) == 0):
			return 0
		return -1

	def getValidLocations(self,grid):
		validLocations=[]
		for i in range(COLUMN_COUNT):
			j = ROW_COUNT-1
			while j >= 0 and grid[j][i] != EMPTY:
				j = j-1
			if j >= 0:
				validLocations.append((j,i))
		return validLocations

	
	def isGameOver(self,grid,turn):
		for i in range(ROW_COUNT):
			for j in range(COLUMN_COUNT-WINDOW_LENGTH+1):
				if(grid[i][j:j+4].count(turn) == WINDOW_LENGTH):
					return True
			
		for i in range(ROW_COUNT-WINDOW_LENGTH+1):
			for j in range(COLUMN_COUNT):
				if([grid[i+c][j] for c in range(4)].count(turn) == WINDOW_LENGTH):
					return True

		for i in range(ROW_COUNT-WINDOW_LENGTH+1):
			for j in range(COLUMN_COUNT-WINDOW_LENGTH+1):
				if([grid[i+c][j+c] for c in range(4)].count(turn) == WINDOW_LENGTH):
					return True

		for i in range(ROW_COUNT-WINDOW_LENGTH+1):
			for j in range(COLUMN_COUNT-WINDOW_LENGTH+1):
				if([grid[i+WINDOW_LENGTH-1-c][j+c] for c in range(4)].count(turn) == WINDOW_LENGTH):
					return True
		
		return False

	def alphaBeta(self, grid, depth, alpha, beta, maximizingPlayer):
		baseScore = self.isTerminalNode(grid)
		if baseScore != -1:
			return (None, baseScore)
		if depth == 0:
			return (None, self.getPostionScore(grid))
		locations = self.getValidLocations(grid)
		if maximizingPlayer:
			bestScore = -math.inf
			bestMove = random.choice(locations)
			for row,col in locations:
				tempGrid = copy.deepcopy(grid)
				tempGrid[row][col] = AI_TURN
				score = self.alphaBeta(tempGrid,depth-1,alpha,beta,False)[1]
				if(score > bestScore):
					bestScore = score
					bestMove = (row,col)
				alpha = max(alpha, bestScore)
				if alpha >= beta:
					break
			return (bestMove,bestScore)
		else:
			worstScore = math.inf
			worstMove = random.choice(locations)
			for row,col in locations:
				tempGrid = copy.deepcopy(grid)
				tempGrid[row][col] = PLAYER_TURN
				score = self.alphaBeta(tempGrid,depth-1,alpha,beta,True)[1]
				if score < worstScore :
					worstScore = score
					worstMove = (row,col)
				beta = min(beta, worstScore)
				if alpha >= beta:
					break
			return (worstMove,worstScore)


