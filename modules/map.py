#Map
#Controls Platforms and Ground objects for the map

import pygame
from settings import *

class Ground(pygame.sprite.Sprite): #Ground class
	def __init__(self, game, rect, platform = 0, texture = None):
		self.rect = rect #store position, rect, texture, and platform or ground variables
		self.game = game
		self.platform = platform
		pygame.sprite.Sprite.__init__(self, game.ground)
		self.speed = 0
		self.dir = 0
		if texture: self.tex = pygame.transform.scale(texture, self.rect[2:])
		else: self.tex = None
	def update(self): #blit self to screen
		if self.tex:self.game.win.blit(self.tex, self.rect)
		else:pygame.draw.rect(self.game.win, BLACK, self.rect)

class Moving(Ground):
	def __init__(self,game,rect,direction,speed,Platform_Range,platform = 1, texture=None):
		Ground.__init__(self,game,rect,1,texture) #store all ground class variables
		self.range = Platform_Range #store variables for movement
		self.speed = speed
		self.dir = direction
		#0 = Left
		#1 = Right
		#2 = Up
		#3 = Down
	def update(self): #move and blit self to screen
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

class TimedGround(Ground):
	def __init__(self,game,rect,direction,speed,end,time,platform = 1, texture=None):
		Ground.__init__(self,game,rect,1,texture) #ground subclass
		self.limit = end #store extra variables for timed ground
		self.start = time
		self.time = time
		self.game = game
		self.update_plat = True
		self.speed = speed
		self.dir = direction
	def update(self): #blit self to screen
		if (1 in [pygame.Rect(x.hitbox).colliderect(self.rect) for x in self.game.sprites] and self.time) or self.time >= self.start-0.5:#destroy if there are no players on the platform or time limit is exceeded
			self.time -= self.game.dt
			if self.time < 0:
				self.time = 0
			if self.dir > 1:
				if self.rect[1] > self.limit:
					self.update_plat = False
			else:
				if self.rect[0] > self.limit:
					self.update_plat = False
			if self.update_plat:
				self.rect = (self.rect[0] + ((self.speed * (self.dir==1)) - (self.speed*(self.dir==0)))*self.game.dt, self.rect[1] - ((self.speed*(self.dir==2))-(self.speed*(self.dir==3)))*self.game.dt,self.rect[2],self.rect[3])
			Ground.update(self)
		else:
			self.kill()
