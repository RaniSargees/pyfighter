import pygame
from random import randint
from settings import *
from paintCanvas import *
from BTN import *


class paint():
	def __init__(self,win):
		self.win = win
		self.BTN = pygame.sprite.Group()
		self.shift = 20
	
	def new(self):
		self.canvas = pygame.Surface((640,480),pygame.SRCALPHA,32)
		self.grid = paintCanvis(self.canvas)
		for i in range(len(COLORS)):
			BTN(self,self.win,i,(30+(i*70)-((i > 8)*630),520+((i > 8)*70),60,60))
			
		self.hold = False
	
	def run(self):
		self.playing = 1
		self.Mouse = pygame.mouse.get_pos()
		self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
		while self.playing:
			events = pygame.event.get()
			self.draw()
			if self.hold:
				self.Mouse2 = pygame.mouse.get_pos()
				self.Mouse2 = (self.Mouse2[0]-self.shift,self.Mouse2[1]-self.shift)
				self.grid.update(self.Mouse,self.Mouse2)
			else:
				self.grid.update()
			for i in self.BTN:
				if i.rect.collidepoint(pygame.mouse.get_pos()):
					if self.hold == True:
						for j in self.BTN:
							j.update(clicked = 0)
						i.update(clicked = 1)
						self.grid.color = i.cnum
						
					else:
						i.update(mOver = 1)
				else:
					i.update()
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.hold = True
				elif event.type == pygame.MOUSEBUTTONUP:
					self.hold = False
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_p:
						self.canvas = pygame.Surface((640,480),pygame.SRCALPHA,32)
						self.grid = paintCanvis(self.canvas)
			self.Mouse = pygame.mouse.get_pos()
			self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
			pygame.time.delay(10)
			pygame.display.update()
	def draw(self):
		self.win.fill(WHITE)
		pygame.draw.line(self.win,BLACK,(17,17),(663,17),6)
		pygame.draw.line(self.win,BLACK,(663,17),(663,503),6)
		pygame.draw.line(self.win,BLACK,(663,503),(17,503),6)
		pygame.draw.line(self.win,BLACK,(17,503),(17,17),6)
		self.win.blit(self.canvas,(self.shift,self.shift))

pygame.init()
win = pygame.display.set_mode(RES)
d = paint(win)
d.new()
d.run()
pygame.quit()