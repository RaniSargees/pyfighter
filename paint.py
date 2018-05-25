import pygame
from random import randint
from settings import *
from paintGrid import *
from paintCanvis import *


class paint():
	def __init__(self,win):
		self.win = win
	
	def new(self):
		self.draw = pygame.display.set_mode(RES)
		self.grid = paintCanvis(self.draw,5,(0,0,1280,720))
		self.hold = False
	
	def run(self):
		self.playing = 1
		self.Mouse = pygame.mouse.get_pos()
		while self.playing:
			events = pygame.event.get()
			self.win.fill(WHITE)
			self.win.blit(self.draw,(0,0))
			if self.hold:
				self.grid.update(self.Mouse,pygame.mouse.get_pos())
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
						self.draw = pygame.display.set_mode(RES)
			self.Mouse = pygame.mouse.get_pos()
			pygame.time.delay(10)
			pygame.display.update()

pygame.init()
win = pygame.display.set_mode(RES)
d = paint(win)
d.new()
d.run()
pygame.quit()