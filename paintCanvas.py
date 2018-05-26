import pygame
from settings import *

class paintCanvis():
	def __init__(self,win,color,brush):
		self.win = win
		self.color = color
		self.brush = brush
		self.colorList = COLORS
		self.drawList = []
	
	def update(self,cord1=None,cord2=None):
		self.win.fill((192,192,192))
		if cord1 != None:
			self.drawList.append([cord1,cord2,self.color,self.brush])
		for i in self.drawList:
			pygame.draw.line(self.win,self.colorList[i[2]],i[0],i[1],i[3])
		