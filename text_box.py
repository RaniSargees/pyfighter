import pygame
from settings import *

class Text_Box(pygame.sprite.Sprite):
	def __init__(self,win,rect,group=None,text='Enter Text Here',title = ''):
		if group != None:
			pygame.sprite.Sprite.__init__(self,group)
		self.win = win
		self.rect = pygame.Rect(rect)
		self.Basetext = text
		self.font = pygame.font.SysFont('Courier New',14)
		self.text = ''
		self.text_display = self.font.render(self.text,1,BLACK)
		self.text_rect = self.text_display.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)))
		if title != '':
			self.title = self.font.render(title,1,BLACK)
			self.title_rect = self.title.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]-7))
		else:
			self.title = 0
		self.textLine = 0

	def update(self,clicked,events=[]):
		pygame.draw.rect(self.win,BLACK,self.rect,1)
		pygame.draw.rect(self.win,BLACK,(self.rect[0]+(self.rect[2]/24),self.rect[1]+(self.rect[3]/12),self.rect[2]-(self.rect[2]/12),self.rect[3]-(self.rect[3]/6)),1)
		if clicked:
			self.textLine += 1
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						self.text = self.text[:-1]
					elif len(self.text)<= 12 and not(event.key == pygame.K_RETURN):
						self.text += event.unicode
			self.text_display = self.font.render(self.text+((self.textLine%90 < 45)*'|')+((self.textLine%90 >= 45)*' '),1,BLACK)
			self.text_rect = self.text_display.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)))
		else:
			if self.textLine != 0:
				self.text_display = self.font.render(self.text,1,BLACK)
				self.text_rect = self.text_display.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)))
			if self.text =='':
				self.text_display = self.font.render(self.Basetext,1,GRAY)
				self.text_rect = self.text_display.get_rect(center=(self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2)))
		if self.title != 0:
			self.win.blit(self.title,self.title_rect)
		self.win.blit(self.text_display,self.text_rect)
