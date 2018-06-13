import pygame
from settings import *

class Ground(pygame.sprite.Sprite):
	def __init__(self, game, rect, platform = 0, texture = None):
		self.rect = rect
		self.game = game
		self.platform = platform
		pygame.sprite.Sprite.__init__(self, game.ground)
		self.speed = 0
		self.dir = 0
		if texture: self.tex = pygame.transform.scale(texture, self.rect[2:])
		else: self.tex = None
	def update(self):
		if self.tex:self.game.win.blit(self.tex, self.rect)
		else:pygame.draw.rect(self.game.win, BLACK, self.rect)

class Moving(Ground):
	def __init__(self,game,rect,direction,speed,Platform_Range,platform = 1, texture=None):
		Ground.__init__(self,game,rect,1,texture)
		self.range = Platform_Range
		self.speed = speed
		self.dir = direction
		#0 = Left
		#1 = Right
		#2 = Up
		#3 = Down
	def update(self):
		self.rect = (self.rect[0] + ((self.speed * (self.dir==1)) - (self.speed*(self.dir==0)))*self.game.dt, self.rect[1] - ((self.speed*(self.dir==2))-(self.speed*(self.dir==3)))*self.game.dt,self.rect[2],self.rect[3])
		if self.dir > 1:
			if self.rect[1] >= max(self.range):
				self.dir = 2
			elif self.rect[1] <= min(self.range):
				self.dir = 3
		else:
			if self.rect[0] >= max(self.range):
				self.dir = 0
			elif self.rect[0] <= min(self.range):
				self.dir = 1
		Ground.update(self)