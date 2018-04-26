import pygame

class Char(pygame.sprite.Sprite):
	def __init__(self,game):
		self.groups = game.sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.x = 200
		self.y = 200
		self.moveSpeed = 400
		self.jumpSpeed = -800
		self.maxJumps = 2
		self.currentJumps = self.maxJumps
		self.vspeed = 0
		self.hspeed = 0
		self.gravity = 28

	def update(self,keys,events):
		self.keys = keys
		self.events = events
		if self.y >= self.game.ground:
			self.currentJumps = self.maxJumps
			self.y = self.game.ground
			self.vspeed = 0
		else: self.vspeed += self.gravity
		self.get_keys()
		self.y += self.vspeed * self.game.dt
		self.x += self.hspeed * self.game.dt
		pygame.draw.rect(self.game.win,(0,0,0),(self.x,self.y,30,50))

	def jump(self):
		if self.currentJumps:
			self.currentJumps -= 1
			self.vspeed = self.jumpSpeed

	def get_keys(self):
		if self.keys[pygame.K_a] and not self.keys[pygame.K_d]:
			self.hspeed = -self.moveSpeed
		elif self.keys[pygame.K_d] and not self.keys[pygame.K_a]:
			self.hspeed = self.moveSpeed
		else: self.hspeed = 0
		for e in self.events:
			if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_w):self.jump();print(1)

