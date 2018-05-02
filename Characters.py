import pygame, math
from Settings import *

class Char(pygame.sprite.Sprite):
	def __init__(self,game,joystick,buttonmap=[0,1,2,3,4,5]):
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
		self.joystick = joystick
		self.buttonmap = buttonmap
		self.dmg = 0
		self.stun = 0
		self.knocked = 0
		self.facing = 0
		#0 = Left
		#1 = Right
		#2 = Up
		#3 = Down
		self.hitbox = (self.x+4,self.y+4,40,64)
	def update(self,keys,events):
		self.hitbox = (self.x+4,self.y+4,40,64)
		self.keys = keys
		self.events = events
		self.grounded = (self.y >= self.game.ground)
		self.inStage = (self.x <= 1130 and self.x >= 102)
		if self.grounded and self.inStage:
			if self.stun <= 0:
				self.knocked = 0
			if self.knocked:
				self.vspeed *= -1
			else:
				self.currentJumps = self.maxJumps
				self.y = self.game.ground
				self.vspeed = 0
		else: self.vspeed += self.gravity * self.gravityMultiplier * (60/max(1,self.game.clock.get_fps()))
		if self.y > 800:
			self.dmg = 0
			self.x = 200+(self.joystick.get_id()*200)
			self.y = 200
			self.vspeed = 0
			self.hspeed = 0
		self.get_keys()
		self.y += self.vspeed * self.game.dt
		self.x += self.hspeed * self.game.dt
		if not(self.inStage) and self.grounded and (self.x <= 1130 and self.x >= 102):
			self.x -= self.hspeed * self.game.dt
		pygame.draw.rect(self.game.win,(RED, GREEN, BLUE, BLACK)[self.joystick.get_id()],(self.x,self.y,48,72))

	def jump(self):
		if self.currentJumps:
			self.currentJumps -= 1
			self.vspeed = self.jumpSpeed
			self.jumpBonus = 0

	def atkLight(self, direction):
		if direction < 2:
			pygame.draw.rect(self.game.win,BLUE,(self.x-20+((direction==1)*(48+20)), self.y, 20, 72),4)
			collisions=[(pygame.Rect((self.x-20+((direction==1)*(48+20)),self.y,20,72)).colliderect(x.hitbox),x)for x in self.game.sprites]
		elif direction >= 2:
			pygame.draw.rect(self.game.win,BLUE,(self.x,self.y-20+((direction==3)*(72+10)),48,30),4)
			collisions=[(pygame.Rect((self.x,self.y-20+((direction==3)*(72+10)),48,30)).colliderect(x.hitbox),x)for x in self.game.sprites]
		for x in collisions:
			if x[0] and not(x[1]==self):
				x[1].knockBack(20,direction)
				x[1].damage(20)
	def atkHeavy(self, direction):self.atkLight(direction)

	def knockBack(self,hit,direction=0):
		#direction represents the direction of the attacking player
		self.gravityMultiplier=1
		self.stun = hit/200
		self.knocked = 1
		vel = (self.dmg+hit)**1.5
		if direction < 2:
			self.hspeed = (direction-0.5)*2*vel*math.cos(math.pi/6) * (60/max(1,self.game.clock.get_fps()))
			self.vspeed = -vel*math.sin(math.pi/6) * (60/max(1,self.game.clock.get_fps()))
		elif direction >= 2:
			self.vspeed = ((direction==3)-0.5)*2*vel*math.sin(math.pi/4) * (60/max(1,self.game.clock.get_fps()))
		self.currentJumps = max(1, self.currentJumps)
		#Don't remove the line below. It fixes the sliding bug
		self.y -= 1

	def damage(self, hit):
		self.dmg+=hit/4

	def get_keys(self):
		if self.stun <= 0:
			if  self.joystick.get_axis(0) < -.5:
				self.hspeed = max(self.hspeed-self.moveSpeed*(60/max(1,self.game.clock.get_fps())), -self.maxMoveSpeed)
				self.facing = 0
			elif self.joystick.get_axis(0) > .5:
				self.hspeed = min(self.hspeed+self.moveSpeed*(60/max(1,self.game.clock.get_fps())), self.maxMoveSpeed)
				self.facing = 1
			elif self.hspeed and not(self.knocked):
				if abs(self.hspeed)>self.moveSpeed: self.hspeed -= (self.hspeed/abs(self.hspeed) * self.moveSpeed * (60/max(1,self.game.clock.get_fps())))/((self.grounded==0)*5+1)
				else: self.hspeed = 0
			self.gravityMultiplier = (self.joystick.get_axis(1) >.9)*2 + 1
			if self.joystick.get_button(self.buttonmap[0]) and (self.vspeed < 0) and (self.jumpBonus < self.maxJumpBonus):
				self.vspeed += self.jumpBonusSpeed * (60/max(1,self.game.clock.get_fps()))
				self.jumpBonus += 1
			for e in self.events:
				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:self.knockBack(60,self.facing) #testing only, remove later
				if e.type == pygame.JOYBUTTONDOWN and e.joy==self.joystick.get_id():
					if e.button == self.buttonmap[0]: self.jump()
					if e.button == self.buttonmap[1]:
						if self.joystick.get_axis(1)> .5: self.atkLight(3)
						elif self.joystick.get_axis(1)<-.5: self.atkLight(2)
						else: self.atkLight(self.facing)
					elif e.button == self.buttonmap[2]:
						if self.joystick.get_axis(1)> .5: self.atkHeavy(3)
						elif self.joystick.get_axis(1)<-.5: self.atkHeavy(2)
						else: self.atkHeavy(self.facing)

		else:
			self.stun -= self.game.dt
