import pygame,numpy,sys
from settings import *
sys.setrecursionlimit(99999999)
class paintCanvis():
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
				#self.sides = [[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0]]
				self.sides = [[1,0],[0,1],[-1,0],[0,-1]]
				self.recursiveFill(list[1])
		self.save = pygame.surfarray.pixels2d(self.win.copy())
		pygame.surfarray.blit_array(self.win,self.save)

	def recursiveFill(self,pos):
		posList = [pos]
		while len(posList) > 0:
			testPos = posList.pop()
			
			if self.win.get_at(testPos) == self.base:
				self.win.set_at(testPos,self.colorList[self.color])
				for i in self.sides:
					posList.append((testPos[0]+i[0],testPos[1]+i[1]))

#if self.win.get_at(pos) == self.base:
#				self.win.set_at(pos,self.colorList[self.color])
#				
#				
#				if dir == 1:
#					self.recursiveFill([pos[0]+1,pos[1]+1],2)
#					self.recursiveFill([pos[0]+0,pos[1]+1],3)
#					self.recursiveFill([pos[0]-1,pos[1]+1],4)
#					self.recursiveFill([pos[0]-1,pos[1]+0],5)
#					self.recursiveFill([pos[0]-1,pos[1]-1],6)
#					self.recursiveFill([pos[0]+0,pos[1]-1],7)
#					self.recursiveFill([pos[0]+1,pos[1]-1],8)
#					self.recursiveFill([pos[0]+1,pos[1]+0],9)
#				elif dir == 2:
#					self.recursiveFill([pos[0]+1,pos[1]+1],2)
#					self.recursiveFill([pos[0]+0,pos[1]+1],3)
#					self.recursiveFill([pos[0]+1,pos[1]+0],9)
#				elif dir == 3:
#					self.recursiveFill([pos[0]+0,pos[1]+1],3)
#				elif dir == 4:
#					self.recursiveFill([pos[0]+0,pos[1]+1],3)
#					self.recursiveFill([pos[0]-1,pos[1]+1],4)
#					self.recursiveFill([pos[0]-1,pos[1]+0],5)
#				elif dir == 5:
#					self.recursiveFill([pos[0]-1,pos[1]+0],5)
#				elif dir == 6:
#					self.recursiveFill([pos[0]-1,pos[1]+0],5)
#					self.recursiveFill([pos[0]-1,pos[1]-1],6)
#					self.recursiveFill([pos[0]+0,pos[1]-1],7)
#				elif dir == 7:
#					self.recursiveFill([pos[0]+0,pos[1]-1],7)
#				elif dir == 8:
#					self.recursiveFill([pos[0]+0,pos[1]-1],7)
#					self.recursiveFill([pos[0]+1,pos[1]-1],8)
#					self.recursiveFill([pos[0]+1,pos[1]+0],9)
#				elif dir == 9:
#					self.recursiveFill([pos[0]+1,pos[1]+0],9)
#			else:
#				return None