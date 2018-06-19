#PaintCanvas
#Contains the surface data for the canvas on paint.py
import pygame
from settings import *
class paintCanvas():
	def __init__(self,win,color,brush):
		self.win = win #store variables for paint canvas
		self.color = color
		self.brush = brush
		self.colorList = COLORS
		self.rect = pygame.Rect(20,20,640,480)
		self.drawList = []
		self.win.fill((192,192,192))
		self.save = self.win.copy()

	def update(self,list = None): #update self surface (draw with brushes)
		#List = [type,required info]
		#types  1 = Line
		#		2 = Circle
		if list != None:
			if list[0] == 1:
				pygame.draw.line(self.win,self.colorList[self.color],list[1],list[2],self.brush)
			elif list[0] == 2:
				pygame.draw.circle(self.win,self.colorList[self.color],list[1],self.brush*2)
		self.save = self.win.copy()

	def flood_fill(self,pos,win=None): #iterative floot fill algorithm
		if win == None:                #recursion was too slow and kept crashing the program
			win = self.win
		pxarray = pygame.PixelArray(win)
		base = win.map_rgb(win.get_at(pos))
		clr = win.map_rgb(self.colorList[self.color])
		if base==clr:return
		posList = set()
		posList.add(pos)
		while len(posList):
			testPos=posList.pop()
			try:pxarray[testPos]
			except:continue
			if pxarray[testPos] == base:
				pxarray[testPos] = clr
				for i in [[1,0],[0,1],[-1,0],[0,-1]]:posList.add((testPos[0]+i[0],testPos[1]+i[1]))
		del pxarray
