import pygame
from settings import *

class BTN(pygame.sprite.Sprite):
	def __init__(self,surface,color,rect,group,clickColor=(0,0,255),text='',fn=None,clickable = True,thickness = 1,image = None,allign = 'center'):
		pygame.sprite.Sprite.__init__(self,group)
		self.win = surface
		self.color = COLORS[color]
		self.cnum = color
		self.outline = clickColor
		self.rect = pygame.Rect(rect)
		self.thickness = thickness
		self.clickable = clickable
		if allign == 'center':
			self.allignment = 0
		elif allign == 'bottom':
			self.allignment = 1
		elif allign == 'top':
			self.allignment = -1
		else:
			self.allignment = 0
		if text != '':
			self.charSize = int((self.rect[2]/len(text)))
			self.font = pygame.font.SysFont('Courier New',self.charSize)
			self.text = self.font.render(text,True,BLACK)
			self.text_rect = self.text.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)+(self.allignment*(self.rect[3]/2-(self.charSize/2)))))
		else:
			self.text = None
		self.fn = str(fn)
		self.image = image
		self.selected = 0
	
	def update(self,mOver = 0,clicked = -1,newText = None, hColor = None):
		if self.image != None:
			self.win.blit(self.image,(self.rect[0],self.rect[1]))
		else:
			pygame.draw.rect(self.win,self.color,self.rect)
		if newText != None:
			self.charSize = int((self.rect[2]/len(newText)))
			self.font = pygame.font.SysFont('Courier New',self.charSize)
			self.text = self.font.render(newText,True,BLACK)
			self.text_rect = self.text.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+((self.rect[3]/2)*self.allignment)))
		if self.text != None:
			self.win.blit(self.text,self.text_rect)

		if clicked != -1:
			self.selected = clicked
		if mOver or self.selected == 1:
			if hColor != None:
				pygame.draw.rect(self.win,hColor,self.rect,self.thickness*3)
			else:
				pygame.draw.rect(self.win,self.outline,self.rect,self.thickness*3)
		else:
			pygame.draw.rect(self.win,BLACK,self.rect,self.thickness)
		
		
		