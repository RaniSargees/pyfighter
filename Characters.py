import pygame, math
from Settings import *

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
		self.dmg = 0
		self.joystick = joystick
		self.stun = 0
		self.face_left = 0
		self.hitbox = (self.x+4,self.y+4,40,64)
	def update(self,keys,events):
		self.hitbox = (self.x+4,self.y+4,40,64)
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
		pygame.draw.rect(self.game.win,(RED, GREEN, BLUE, BLACK)[self.joystick.get_id()],(self.x,self.y,48,72))

	def jump(self):
		if self.currentJumps:
			self.currentJumps -= 1
			self.vspeed = self.jumpSpeed
			self.jumpBonus = 0

	def atkLight(self):
		pygame.draw.rect(self.game.win,RED,(self.x-20+((self.face_left==0)*(48+20)), self.y, 20, 72),4)
		collisions=[(pygame.Rect((self.x-20+((self.face_left==0)*(48+20)),self.y,20,72)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[x[1].knockBack(50*-(self.face_left-.5)*2) for x in collisions if x[0]]
	def atkHeavy(self):self.atkLight()

	def knockBack(self,hit):
		self.stun = hit/200
		vel = (self.dmg+abs(hit))**1.5
		self.hspeed = (hit/abs(hit))*vel*math.cos(math.pi/6)
		self.vspeed = -vel*math.sin(math.pi/6)
		self.currentJumps = max(1, self.currentJumps)
		self.dmg+=abs(hit/4)
		print(self.dmg)

	def get_keys(self):
		if self.stun <= 0:
			if  self.joystick.get_axis(0) < -.5 and -self.hspeed < self.maxMoveSpeed:
				self.hspeed -=self.moveSpeed
				self.face_left = 1
			elif self.joystick.get_axis(0) > .5 and self.hspeed < self.maxMoveSpeed:
				self.hspeed += self.moveSpeed
				self.face_left = 0
			elif self.hspeed: self.hspeed -= self.hspeed/abs(self.hspeed)*min(self.moveSpeed, abs(self.hspeed))
			self.gravityMultiplier = (self.joystick.get_axis(1)>.75)*2+1
			for e in self.events:
				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:self.knockBack(60) #testing only, remove later
				if e.type == pygame.JOYBUTTONDOWN and e.joy==self.joystick.get_id():
					if e.button == 0: self.jump()
					if e.button == 1: self.atkLight()
					if e.button == 2: self.atkHeavy()
			if self.joystick.get_button(0) and (self.vspeed < 0) and (self.jumpBonus < self.maxJumpBonus):
				self.vspeed += self.jumpBonusSpeed
				self.jumpBonus += 1
		else:
			self.stun -= self.game.dt
