import pygame
from settings import *

class BTN(pygame.sprite.Sprite):
	def __init__(self,game,surface,color,rect,clickColor=(0,0,255),text=''):
		self.game = game
		pygame.sprite.Sprite.__init__(self,self.game.BTN)
		self.win = surface
		self.color = COLORS[color]
		self.cnum = color
		self.outline = clickColor
		self.rect = pygame.Rect(rect)
		self.text = text
		self.selected = 0
	
	def update(self,mOver = 0,clicked = -1):
		pygame.draw.rect(self.win,self.color,self.rect)
		if clicked != -1:
			self.selected = clicked
		if mOver or self.selected == 1:
			pygame.draw.rect(self.win,self.outline,self.rect,3)
		else:
			pygame.draw.rect(self.win,BLACK,self.rect,1)
		
		
		