import pygame, math

class Char(pygame.sprite.Sprite):
	def __init__(self,game,joystick):
		self.groups = game.sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.x = 200
		self.y = 200
		self.maxMoveSpeed = 400
		self.moveSpeed = 60
		self.jumpSpeed = -500
		self.jumpBonusSpeed = -30
		self.maxJumps = 2
		self.jumpBonus = 0
		self.maxJumpBonus = 10
		self.currentJumps = self.maxJumps
		self.vspeed = 0
		self.hspeed = 0
		self.gravity = 32
		self.gravityMultiplier = 1
		self.dmg = 40
		self.joystick = joystick
	def update(self,keys,events):
		self.keys = keys
		self.events = events
		self.grounded = (self.y >= self.game.ground)
		if self.grounded:
			self.currentJumps = self.maxJumps
			self.y = self.game.ground
			self.vspeed = 0
		else: self.vspeed += self.gravity * self.gravityMultiplier
		self.get_keys()
		self.y += self.vspeed * self.game.dt
		self.x += self.hspeed * self.game.dt
		pygame.draw.rect(self.game.win,(0,0,0),(self.x,self.y,30,50))

	def jump(self):
		if self.currentJumps:
			self.currentJumps -= 1
			self.vspeed = self.jumpSpeed
			self.jumpBonus = 0

	def knockBack(self,hit):
		vel = (self.dmg+abs(hit))**1.5
		self.hspeed = (hit/abs(hit))*vel*math.cos(math.pi/4)
		self.vspeed = -vel*math.sin(math.pi/4)

	def get_keys(self):
		if  self.joystick.get_axis(0) < -.5 and -self.hspeed < self.maxMoveSpeed:
			self.hspeed -=self.moveSpeed
		elif self.joystick.get_axis(0) > .5 and self.hspeed < self.maxMoveSpeed:
			self.hspeed += self.moveSpeed
		elif self.hspeed and self.grounded: self.hspeed -= self.hspeed/abs(self.hspeed)*min(self.moveSpeed, abs(self.hspeed))
		self.gravityMultiplier = ((bool(self.keys[pygame.K_s]) or self.joystick.get_axis(1)>.75)*2)+1
		for e in self.events:
			if e.type == pygame.KEYDOWN and e.key == pygame.K_p:self.knockBack(60) #testing only, remove later
			if e.type == pygame.JOYBUTTONDOWN and e.button==0:self.jump()
		if self.joystick.get_button(0) and (self.vspeed < 0) and (self.jumpBonus < self.maxJumpBonus):
			self.vspeed += self.jumpBonusSpeed
			self.jumpBonus += 1
