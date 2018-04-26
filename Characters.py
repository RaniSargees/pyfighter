import pygame

class Char(pygame.sprite.Sprite):
	def __init__(self,game):
		self.groups = game.sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.x = 200
		self.y = 200
		self.spd = 400
		self.jumpTotal = 2
		self.jumpL = self.jumpTotal
		self.jumping = False
		self.jumpTime = 0.8

	def update(self,keys):
		self.keys = keys
		self.get_keys()
		if self.jumping == True:
			self.jumpVar -= self.game.dt
			self.y -= ((self.jumpVar*50)**2) * self.game.dt
			if self.jumpVar <= 0:
				self.jumping = False
		self.y += 500 * self.game.dt
		if self.y > self.game.ground:
			self.jumpL = self.jumpTotal
			self.y = self.game.ground
		pygame.draw.rect(self.game.win,(0,0,0),(self.x,self.y,30,50))

	def jump(self):
		if self.jumping == False and self.jumpL:
			self.jumpVar = self.jumpTime
			self.jumping = True
			self.jumpL -= 1

	def get_keys(self):
		if self.keys[pygame.K_a]:
			self.x -= self.spd * self.game.dt
		if self.keys[pygame.K_d]:
			self.x += self.spd * self.game.dt
		if self.keys[pygame.K_w] or self.keys[pygame.K_SPACE]:
			if self.keyhold == False:
				self.keyhold = True
				self.jump()
		else:
			self.keyhold = False
			self.jumping = False

