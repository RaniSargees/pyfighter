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
		self.inStage = 0
		self.hit_list = [self]
		self.AbilTime = 0
		self.AbilAir = 0
		self.AbilRun = -1
		self.Release = 0
		self.dmg = 0
		self.stun = 0
		self.knocked = 0
		self.freeze=0
		self.facing = 0
		#0 = Left
		#1 = Right
		#2 = Up
		#3 = Down
		self.hitbox = (self.x+4-24,self.y+4-72,40,64)

	def update(self,keys,events):
		self.keys = keys
		self.events = events
		self.grounded = [x for x in self.game.ground if pygame.Rect(x.rect).collidepoint(self.x, self.y)]
		self.touch_ground = [x for x in self.game.ground if pygame.Rect(x.rect).colliderect((self.x-(48/2),self.y-72,48,72))]
		self.inStage = False
		for i in self.grounded:
			self.inStage = (self.x <= (i.rect[0]+i.rect[2]) and self.x >= i.rect[0])
	
		if self.grounded:
			if self.stun <= 0:
				self.knocked = 0
			if self.knocked:
				self.vspeed *= -1
			else:
				self.AbilAir = 0
				self.currentJumps = self.maxJumps
				self.vspeed = 0
				self.y=self.grounded[0].rect[1]
				if self.grounded[0].platform and self.gravityMultiplier == 3:
					self.y += self.grounded[0].rect[3]
		else: self.vspeed += self.gravity * self.gravityMultiplier * (60/max(1,self.game.clock.get_fps()))
		if self.y > 800:
			self.dmg = 0
			self.x = 200+(self.joystick.get_id()*200)
			self.y = 200
			self.vspeed = 0
			self.hspeed = 0
		self.get_keys()
		if self.AbilRun >= 0:
			if self.AbilTime > 0 or self.AbilTime == -1:
				if self.AbilTime > 0:
					self.AbilTime -= self.game.dt
				exec(['self.RunSpecial0()','self.RunSpecial1()','self.RunSpecial2()','self.RunSpecial3()'][self.AbilRun])
			else:
				self.atkEnd()
		else:
			self.hit_list = [self]
		self.y += self.vspeed * self.game.dt
		self.x += self.hspeed * self.game.dt
		try:
			if not(self.inStage) and self.touch_ground and not(self.touch_ground[0].platform) and (self.x <= (self.touch_ground[0].rect[0]+self.touch_ground[0].rect[2]) and self.x >= self.touch_ground[0].rect[0]):
				self.x -= self.hspeed * self.game.dt
		except:
			None
		self.hitbox = (self.x+4-24,self.y+4-72,40,64)
		
		pygame.draw.rect(self.game.win,(RED, GREEN, BLUE, BLACK)[self.joystick.get_id()],(self.x-48/2,self.y-72,48,72))
		pygame.draw.rect(self.game.win, BLACK, self.hitbox)
	def jump(self):
		if self.currentJumps:
			self.currentJumps -= 1
			self.vspeed = self.jumpSpeed
			self.jumpBonus = 0

	def atkLight(self, direction):
		if direction == 4:
			direction = self.facing
		if direction < 2:
			pygame.draw.rect(self.game.win,BLUE,(self.x-48+((direction==1)*(48+20)), self.y-72, 20, 72),4)
			collisions=[(pygame.Rect((self.x-48+((direction==1)*(48+20)),self.y-72,20,72)).colliderect(x.hitbox),x)for x in self.game.sprites]
		elif direction >= 2:
			pygame.draw.rect(self.game.win,BLUE,(self.x-24,self.y-92+((direction==3)*(72+10)),48,30),4)
			collisions=[(pygame.Rect((self.x-24,self.y-92+((direction==3)*(72+10)),48,30)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(6, direction),x[1].damage(5))for x in collisions if x[0] and x[1]!=self]

	def knockBack(self,hit,direction=0):
		#direction represents the direction of the attacking player
		self.AbilAir=0
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
		self.y -= 5

	def atkEnd(self):
		if not(self.AbilTime == -1):
			self.AbilTime = 0
			self.AbilRun = -1

	def damage(self, hit):
		self.dmg+=hit

	def get_keys(self):
		if self.stun <= 0:
			if  self.joystick.get_axis(0) < -.5:
				self.hspeed = max(self.hspeed-self.moveSpeed*(60/max(1,self.game.clock.get_fps())), -self.maxMoveSpeed) * (abs((self.freeze==0)-0.2)+0.2)
				self.facing = 0
			elif self.joystick.get_axis(0) > .5:
				self.hspeed = min(self.hspeed+self.moveSpeed*(60/max(1,self.game.clock.get_fps())), self.maxMoveSpeed) * (abs((self.freeze==0)-0.2)+0.2)
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
					if e.button == self.buttonmap[2]:
						if self.joystick.get_axis(1)> .5: self.atkLight(3)
						elif self.joystick.get_axis(1)<-.5: self.atkLight(2)
						elif abs(self.joystick.get_axis(0))>.5: self.atkLight(self.facing)
						else: self.atkLight(4)
					elif e.button == self.buttonmap[1]:
						if self.joystick.get_axis(1)> .5: self.atkHeavy(3)
						elif self.joystick.get_axis(1)<-.5: self.atkHeavy(2)
						elif abs(self.joystick.get_axis(0))>.5: self.atkHeavy(self.facing)
						else: self.atkHeavy(4)
				elif e.type == pygame.JOYBUTTONUP and e.joy==self.joystick.get_id():
					if e.button == self.buttonmap[1]:
						self.Release = 1

		else:
			self.stun -= self.game.dt


class Mage(Char):
	def atkHeavy(self,direction):
		exec(['self.special1(direction)','self.special1(direction)','self.special2()','self.special3()','self.special0()'][direction])

	def special0(self):
		if not self.AbilRun+1:
			self.Release = 0
			self.SP0Timer = 0
			self.SP0GO = 0
			self.freeze=1
			self.AbilRun = 0
			self.AbilTime = -1
			self.explosion = self.game.effects['Explosion'].copy()
			self.SP0Len = len(self.explosion)
			self.SP0Count = 0

	def RunSpecial0(self):
		if self.Release and not(self.SP0Count):
			self.SP0GO = 1
			scale = min(int(self.SP0Timer * 400 + 150),400)
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale,scale))
			self.LocNow = (self.x-((self.facing==0)*scale)+((self.facing==1)*(40)),self.y-(scale))
			self.scale = scale
		else:
			self.SP0Timer += self.game.dt
			if self.SP0Timer > 1: self.Release=1;
		if self.SP0GO:
			if self.SP0Count < self.SP0Len:
				self.game.win.blit(self.explosion[self.SP0Count],self.LocNow)
				if self.SP0Count <= 8:
					#Change the spawn location dependant on variable scale
					pygame.draw.rect(self.game.win,BLUE,(self.LocNow[0]+(self.scale/4),self.LocNow[1]+(self.scale/4),self.scale/2,3*self.scale/4),4)
					collisions=[(pygame.Rect((self.LocNow[0]+(self.scale/4),self.LocNow[1]+(self.scale/4),self.scale/2,3*self.scale/4)).colliderect(x.hitbox),x)for x in self.game.sprites]
				else: collisions = [];self.freeze=0
				self.SP0Count += 1
				[(x[1].knockBack((self.scale//10), self.facing),x[1].damage(self.scale//10))for x in collisions if x[0] and not(x[1] in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.AbilRun = -1
				self.AbilTime = 0
				self.Release = 0



	def special1(self,direction):
		print(1)
	def RunSpecial1(self):
		pass

	def special2(self):
		if self.AbilRun+1 == 0 and not(self.AbilAir):
			self.AbilAir = 1
			size = 175
			self.AbilRun = 2
			self.AbilTime = 0.3
			self.SP2Count = 0
			self.explosion = self.game.effects['old_Explosion'].copy()
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.flip(pygame.transform.scale(j,(size,size)),self.facing,1)
			self.LocNow = (self.x-size/2,self.y-size/2)
	def RunSpecial2(self):
		#Add Flame effect and hit box around character
		self.vspeed = -800
		self.gravityMultiplier = 12
		if self.SP2Count < len(self.explosion*2):
			self.game.win.blit(self.explosion[self.SP2Count//2],self.LocNow)
			self.SP2Count += 1
		pygame.draw.rect(self.game.win,BLUE,(self.LocNow[0]+43.75,self.LocNow[1]+43.75,87.5,116.667),4)
		collisions=[(pygame.Rect((self.LocNow[0]+43.75,self.LocNow[1]+43.75,87.5,116.667)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(12, 3),x[1].damage(16))for x in collisions if x[0] and not(x[1] in self.hit_list)]
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
		if self.hit_list != [self]:
			self.AbilAir = False
		

	def special3(self):
		#Drop lightning
		print(3)
	def RunSpecial3(self):
		pass


