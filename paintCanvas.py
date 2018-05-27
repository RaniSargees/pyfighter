import pygame,numpy,sys
from settings import *
sys.setrecursionlimit(99999999)
class paintCanvas():
	def __init__(self,win,color,brush):
		self.win = win
		self.color = color
		self.brush = brush
		self.colorList = COLORS
		self.rect = pygame.Rect(20,20,640,480)
		self.drawList = []
		self.win.fill((192,192,192))
		self.save = pygame.surfarray.pixels2d(self.win.copy())

	def update(self,list = None):
		#List = [type,required info]
		#types 1 = Line
		#	   2 = Circle
		#	   3 = Fill
		if list != None:
			if list[0] == 1:
				pygame.draw.line(self.win,self.colorList[self.color],list[1],list[2],self.brush)
			elif list[0] == 2:
				pygame.draw.circle(self.win,self.colorList[self.color],list[1],self.brush)
			elif list[0] == 3:
				self.base = self.win.get_at(list[1])
				self.sides = [[1,0],[0,1],[-1,0],[0,-1]]
				self.recursiveFill(list[1])
		self.save = pygame.surfarray.pixels2d(self.win.copy())
		pygame.surfarray.blit_array(self.win,self.save)

	def recursiveFill(self,pos):
		pxarray = pygame.PixelArray(self.win)
		base = self.win.map_rgb(self.base)
		clr = self.win.map_rgb(self.colorList[self.color])
		posList = set()
		posList.add(pos)
		while len(posList):
			testPos=posList.pop()
			try:pxarray[testPos]
			except:continue
			if pxarray[testPos] == base:
				pxarray[testPos] = clr
				for i in self.sides:posList.add((testPos[0]+i[0],testPos[1]+i[1]))
		del pxarray
