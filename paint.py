import pygame
from random import randint
from settings import *
from paintCanvis import *


class paint():
	def __init__(self,win):
		self.win = win
		self.shift = 20
	
	def new(self):
		self.canvis = pygame.Surface((640,480),pygame.SRCALPHA,32)
		self.grid = paintCanvis(self.canvis)
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
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.hold = True
				elif event.type == pygame.MOUSEBUTTONUP:
					self.hold = False
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_p:
						self.canvis = pygame.Surface((640,480),pygame.SRCALPHA,32)
						self.grid = paintCanvis(self.canvis)
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
		self.win.blit(self.canvis,(self.shift,self.shift))

pygame.init()
win = pygame.display.set_mode(RES)
d = paint(win)
d.new()
d.run()
pygame.quit()