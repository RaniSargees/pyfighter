import pygame
from settings import *

class BTN(pygame.sprite.Sprite):
	def __init__(self,game,surface,color,rect,group,clickColor=(0,0,255),text='',fn=None,clickable = True):
		self.game = game
		pygame.sprite.Sprite.__init__(self,group)
		self.win = surface
		self.color = COLORS[color]
		self.cnum = color
		self.outline = clickColor
		self.rect = pygame.Rect(rect)
		self.clickable = clickable
		if text != '':
			self.charSize = int((self.rect[2]/len(text)))
			self.font = pygame.font.SysFont('Courier New',self.charSize)
			self.text = self.font.render(text,True,BLACK)
			self.text_rect = self.text.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)))
		else:
			self.text = None
		self.fn = fn
		self.selected = 0
	
	def update(self,mOver = 0,clicked = -1,newText = None):
		pygame.draw.rect(self.win,self.color,self.rect)
		
		if newText != None:
			self.charSize = int((self.rect[2]/len(newText)))
			self.font = pygame.font.SysFont('Courier New',self.charSize)
			self.text = self.font.render(newText,True,BLACK)
			self.text_rect = self.text.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)))
		if self.text != None:
			self.win.blit(self.text,self.text_rect)

		if clicked != -1:
			self.selected = clicked
		if mOver or self.selected == 1:
			pygame.draw.rect(self.win,self.outline,self.rect,3)
		else:
			pygame.draw.rect(self.win,BLACK,self.rect,1)
		
		
		