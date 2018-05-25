########################GRID##########################
#			GRID CLASSES BY: RYOTA PARSONS			 #	 
#													 #	 
#Function: the grid class takes in the rows and		 #
#	collums and their origin coordinates and creates #
#	a grid with the coordinates and the width and	 # 
#	height. The above mentioned variables are send	 #
#	back, to be used by other functions methods and	 #
#	lines of code.									 #
#													 #
#Input Specifications: Rows, Collums, Origin Coords, #
#	Total Height and Width, spacing, and group to be #
#	put into. (Opitional)							 #
#													 #
#			MENU, WORDLIST, AND LETTERGRID			 #
#													 #
#Function: Enherits Grid Class. Takes in grid coords #
#	and applies them to the BTN Class and creates a	 #
#	grid of buttons.								 #
#													 #
#Note: Each class has slightly different functions	 #
#	and parameters to create grids with different	 #
#	purposes.										 #
######################################################

import pygame
from BTN import *
class grid(pygame.sprite.Sprite):
	def __init__(self,width,height,x,y,Xsize,Ysize,spacing,sprites):
		#Width&height are num of buttons in each set
		try:
			#Attemps to put its self into the passed sprite group.
			#If no group is passed it will fail by default
			pygame.sprite.Sprite.__init__(self)
			sprites.add(self)
		except:
			pass
		self.w = width
		self.h = height
		self.Xcord = x
		self.Ycord = y
		self.Xsize = Xsize
		self.Ysize = Ysize
		self.spacing = spacing
		self.makegrid()
	def makegrid(self):
		#Determine the X, Y coordinate and the size for each item in the grid
		self.cords = []
		self.Xint = (self.Xsize + self.spacing) / self.w
		self.Yint = (self.Ysize + self.spacing) / self.h
		self.Xbtn = self.Xint - self.spacing
		self.Ybtn = self.Yint - self.spacing
		for i in range(self.h):
			temp = []
			for j in range(self.w):
				temp.append((self.Xcord + self.Xint*j,self.Ycord + self.Yint*i))
			self.cords.append(temp)


class Menu(grid):
	def __init__(self,win,width,height,x,y,Xsize,Ysize,spacing,values,Fn = None, MaxFont = False, setting = 1,highlight = None,group = None, Font = None):
		grid.__init__(self,width,height,x,y,Xsize,Ysize,spacing,group)
		self.win = win
		self.values = values
		self.MenuList = []
		if Fn == None:
			#Change Fn value to satisfy the BTN classes input specifications
			Fn = ['None' for x in range(self.width*self.height)]
		for i in range(self.h):
			for j in range(self.w):
				#Create all button instances and append them into a list
				self.MenuList.append(BTN(self.win,(255,255,255),self.values[(i*self.w)+j],self.cords[i][j],(self.Xbtn,self.Ybtn),setting = setting,Fn = Fn[(i*self.w)+j],MaxFont = MaxFont, MouseColor = highlight, Font = Font))
	def update(self,mDown = False):
		#v for value. pass mDown as true if the mouse button is down.
		if mDown:
			v = mDown + 2
		else:
			v = 0
		#Update all buttons
		for i in self.MenuList:
			i.update(v)


class WordList(grid):
	def __init__(self,win,width,height,x,y,Xsize,Ysize,spacing,values,group = None):
		grid.__init__(self,width,height,x,y,Xsize,Ysize,spacing, group)
		self.values = values
		self.win = win
		self.AnsKey = []
		for i in range(self.h):
			for j in range(self.w):
				#Create all button instances and append them into a list
				self.AnsKey.append(BTN(self.win,(255,255,255),self.values[(i*self.w)+j],self.cords[i][j],(self.Xbtn,self.Ybtn),setting = 2,Font = 24))
	def update(self, mDown = False):
		if mDown:
			v = mDown + 2
		else:
			v = 0
		#Update all butons
		for i in self.AnsKey:
			i.update(v)



class LetterGrid(grid):
	def __init__(self,win,width,height,x,y,Xsize,Ysize,spacing,values=None,group = None):
		grid.__init__(self,width,height,x,y,Xsize,Ysize,spacing, group)
		self.values = values
		self.win = win
		self.LetterBTN = []
		for i in range(height):
			for j in range(width):
				#Create all button instances and append them into a list
				if self.values != None:
					value = self.values[i][j]
				else:
					value = ' '
				self.LetterBTN.append(BTN(self.win,(255,255,255),value,self.cords[i][j],(self.Xbtn,self.Ybtn),setting = 0,MouseColor = (255,255,0)))
	def update(self,mDown = False):
		if mDown:
			v = mDown+2
		else:
			v = 0
		#Update all buttons and put all state values of each button into a list
		self.ReturnBTN = []
		for i in self.LetterBTN:
			self.ReturnBTN.append(i.update(v))
