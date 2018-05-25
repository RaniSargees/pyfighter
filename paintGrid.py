import pygame,math
from settings import *

class paintGrid():
	def __init__(self,win,psize,rect):
		self.win = win
		self.psize = psize
		self.rect = rect
		self.brush = 1
		self.createGrid()

	def createGrid(self):
		#Amount of pixels within grid
		self.w = self.rect[2]//self.psize
		self.h = self.rect[3]//self.psize
		print(self.w,self.h)
		self.canvis = []
		for i in range(self.h):
			row = []
			for j in range(self.w):
				row.append(0)
			self.canvis.append(row)
	
	def update(self,cords = None,cords2 = None):
		if cords != None:
			if cords != cords2:
				cordList = []
				divValue = math.sqrt(((cords2[0]-cords[0])**2)+((cords2[1]-cords[1])**2))/self.psize
				LineInterval = ((cords2[0]-cords[0])/divValue,(cords2[1]-cords[1])/divValue)
				for i in range(int(divValue)):
					x = cords[0]+(i*LineInterval[0])
					y = cords[1]+(i*LineInterval[1])
					self.change = (int((x-self.rect[0])/self.psize),int((y-self.rect[1])/self.psize))
					self.canvis[self.change[1]][self.change[0]] = self.brush
				self.change = (int((cords2[0]-self.rect[0])/self.psize),int((cords2[1]-self.rect[1])/self.psize))
				self.canvis[self.change[1]][self.change[0]] = self.brush
			else:
				self.change = (int((cords[0]-self.rect[0])/self.psize),int((cords[1]-self.rect[1])/self.psize))
				self.canvis[self.change[1]][self.change[0]] = self.brush
		self.draw()
		
	def draw(self):
		for y,i in enumerate(self.canvis):
			for x,j in enumerate(i):
				#print((WHITE,RED)[j])
				pygame.draw.rect(self.win,(WHITE,RED)[j],((x*self.psize)+self.rect[0],(y*self.psize)+self.rect[1],self.psize,self.psize))
				
	