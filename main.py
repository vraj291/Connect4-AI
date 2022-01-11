from tkinter import Tk,Canvas,BOTH
from constants import AI_TURN, COLUMN_COUNT
from game import Connect4
import math
import time

class MainFrame:

	def __init__(self):
		self.frame=Tk()
		self.frame.geometry('720x750')
		self.frame.title('Connect 4')
		self.canvas = Canvas(self.frame,bg="black")
		self.length = 750
		self.breadth = 720
		self.size = 100
		self.padding = 8
		self.currentDisk = None
		self.game = Connect4()
		self.createBoard()
		self.bindEvents()
		self.frame.mainloop()

	def setCurrentDisk(self,col = None):
		if col == None:
			col = math.floor(COLUMN_COUNT/2)
		if self.currentDisk:
			self.canvas.delete(self.currentDisk)
		color = self.game.getTurnColor()
		self.currentDisk = self.canvas.create_oval(
			10 + (col*self.size) + self.padding,
			28,
			10 + ((col+1)*self.size) - self.padding,
			112,
			fill=color
		)	

	def addDisk(self,row,col):
		color = self.game.getTurnColor()
		self.canvas.create_oval(
			10 + (col*self.size + self.padding),
			140 + (row*self.size + self.padding),
			10 + ((col+1)*self.size - self.padding),
			140 + ((row+1)*self.size - self.padding),
			fill=color
		)

	def createBoard(self):
		self.canvas.create_rectangle(0,130,self.breadth,self.length,fill = 'blue')
		for i in range(0,6):
			for j in range(0,7):
				self.canvas.create_oval(
					10 + (j*self.size + self.padding),
					140 + (i*self.size + self.padding),
					10 + (j+1)*self.size - self.padding,
					140 + (i+1)*self.size - self.padding,
					fill='black'
				)
		self.canvas.pack(fill=BOTH,expand=1)
		self.setCurrentDisk()
		if self.game.getTurn() == AI_TURN:
			time.sleep(200)
			self.makeAIMove()

	def displayWinner(self):
		text = "Human Won !!!!"
		if self.game.getTurn() == AI_TURN:
			text = "AI Won !!!!"
		self.canvas.create_text(360, 75, text=text, fill="white", font=('Helvetica 40 bold'))
		if self.currentDisk:
			self.canvas.delete(self.currentDisk)
		
	def displayGameOver(self):
		self.canvas.create_text(360, 75, text="Game Over !!!", fill="white", font=('Helvetica 40 bold'))
		if self.currentDisk:
			self.canvas.delete(self.currentDisk)

	def setStart(self,event):
		col = math.floor(event.x/self.size)
		if self.game.isValidCol(col):
			self.setCurrentDisk(col)

	def makeAIMove(self):
		self.unbindEvents()
		row,col = self.game.makeAIMove()
		self.addDisk(row,col)
		if self.game.makeMove(row,col):
			self.displayWinner()
			return
		self.game.updateTurn()
		self.setCurrentDisk()
		self.bindEvents()

	def dropDisk(self,event):
		col = math.floor(event.x/self.size)
		row,isValid = self.game.getRow(col)
		if not isValid:
			return
		self.addDisk(row,col)
		if self.game.makeMove(row,col):
			self.displayWinner()
			self.unbindEvents()
			return
		self.game.updateTurn()
		self.setCurrentDisk()
		self.makeAIMove()

	def bindEvents(self):
		self.frame.bind('<Motion>',self.setStart)
		self.frame.bind('<Button-1>',self.dropDisk)
	
	def unbindEvents(self):
		self.frame.unbind('<Motion>')
		self.frame.unbind('<Button-1>')

if __name__ == "__main__":
	MainFrame()
