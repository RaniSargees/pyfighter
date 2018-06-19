#		BTN
#Creates button objects with run able functions

import pygame
from settings import *

class BTN(pygame.sprite.Sprite):
	def __init__(self,surface,color,rect,group,clickColor=(0,0,255),text='',fn=None,clickable = True,thickness = 1,image = None,allign = 'center',circle = 0):
		pygame.sprite.Sprite.__init__(self,group)#set its sprite group
		self.win = surface
		self.color = COLORS[color]
		self.cnum = color#Sets its color
		self.outline = clickColor#Outline color
		self.rect = pygame.Rect(rect)
		self.thickness = thickness#Thickness of its border
		self.clickable = clickable#If the object will stay highlighted (selected) after being clicked
		self.hColor = None
		self.circle = circle
		if allign == 'center':#Text alignment
			self.allignment = 0
		elif allign == 'bottom':
			self.allignment = 1
		elif allign == 'top':
			self.allignment = -1
		else:
			self.allignment = 0
		if text != '':#If there is text create text to blit 
			self.charSize = int((self.rect[2]/len(text)))
			self.font = pygame.font.SysFont('Courier New',self.charSize)
			self.text = self.font.render(text,True,BLACK)
			self.text_rect = self.text.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)+(self.allignment*(self.rect[3]/2-(self.charSize/2)))))
		else:
			self.text = None
		self.fn = str(fn)#Saves passed function
		self.image = image
		self.selected = 0
	
	def update(self,mOver = 0,clicked = -1,newText = None, hColor = None):
		#mOver -----if the mouse if over the object
		#clicked ---if the object has been clicked
		#newText ---Update the text of the button
		#hColor ----Changes the highlight color of the button
		if mOver or clicked+1:
			self.hColor = hColor
		if self.image != None:#if there is an image blit it
			self.win.blit(self.image,(self.rect[0],self.rect[1]))
		else:
			if self.circle:#if the button is a circle blit a circle button instead
				pygame.draw.circle(self.win,self.color,(self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)),self.rect[2]//2)
			else:#otherwise just draw a rectangle
				pygame.draw.rect(self.win,self.color,self.rect)
		if newText != None:#Updates text to newText if newText has something in it
			self.charSize = int((self.rect[2]/len(newText)))
			self.font = pygame.font.SysFont('Courier New',self.charSize)
			self.text = self.font.render(newText,True,BLACK)
			self.text_rect = self.text.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)+(self.allignment*(self.rect[3]/2-(self.charSize/2)))))
		if self.text != None:#blits text if there exists text
			self.win.blit(self.text,self.text_rect)
		if clicked != -1:#Change its selection status if clicked is not -1 (its default)
			self.selected = clicked
		if mOver or self.selected == 1:#If the mouse is hovering or if the button is selected highlight the button
			if self.hColor != None:#use hColor if it exists
				if self.circle:#draw a circle if the button is a circle
					pygame.draw.circle(self.win,self.hColor,(self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)),(self.rect[2]//2),(self.thickness*3))
				else:
					pygame.draw.rect(self.win,self.hColor,self.rect,self.thickness*3)
			else:#Otherwise just use original highlight color
				if self.circle:
					pygame.draw.circle(self.win,self.outline,(self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)),(self.rect[2]//2),(self.thickness*3))
				else:
					pygame.draw.rect(self.win,self.outline,self.rect,self.thickness*3)
		else:#If its not selected and there is no mouse over it draw a black border
			if self.circle:
				pygame.draw.circle(self.win,BLACK,(self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)),(self.rect[2]//2),(self.thickness))
			else:
				pygame.draw.rect(self.win,BLACK,self.rect,self.thickness)
		
		
		