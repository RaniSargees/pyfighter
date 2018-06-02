import pygame, math
from random import randint
from settings import *
from map import *

class Char(pygame.sprite.Sprite):
	def __init__(self,game,joystick,char,buttonmap=[0,1,2,3,4,5]):
		self.groups = game.sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.sprite_image = self.game.char_sprites[char]
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
		self.ability_time = 0
		self.ability_air = 0
		self.ability_run = -1
		self.release = 0
		self.dmg = 0
		self.stun = 0
		self.knocked = 0
		self.freeze = 0
		self.facing = 0
		#0 = Left
		#1 = Right
		#2 = Up
		#3 = Down
		self.hitbox = (self.x+4-24,self.y+4-72,40,68)
		
		#Stats
		self.defense = 5
		self.atttack = None
		self.speed = None

	def update(self,keys,events):
		self.keys = keys
		self.events = events
		self.grounded = [x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.x-self.hitbox[2]//2+1, self.y, self.hitbox[2]-2, 1)]
		self.inStage = False
		for i in self.grounded:
			self.inStage = (self.x <= (i.rect[0]+i.rect[2]) and self.x >= i.rect[0])
		if self.grounded:
			if self.stun <= 0:
				self.knocked = 0
			if self.knocked and self.grounded[0].platform==0:
				self.hspeed *= 0.1
				self.vspeed *= -1
				self.stun = 0
			else:
				self.ability_air = 0
				self.currentJumps = self.maxJumps
				if self.vspeed>0:self.vspeed=0
				self.y=self.grounded[0].rect[1]
				if len(self.grounded) and self.gravityMultiplier == 3 and not len([x for x in self.grounded if not x.platform]):
					self.y += self.grounded[0].rect[3] + self.grounded[0].speed * self.game.dt * (self.grounded[0].dir > 1)
				self.x += self.grounded[0].speed*((self.grounded[0].dir==0)*-1 + (self.grounded[0].dir==1))*self.game.dt
				self.y += self.grounded[0].speed*(self.grounded[0].dir==3)*self.game.dt
		else: self.vspeed += self.gravity * self.gravityMultiplier * (60/max(1,self.game.clock.get_fps()))
		if self.y > 800:
			self.dmg = 0
			self.x = 200+(self.joystick.get_id()*200)
			self.y = 200
			self.vspeed = 0
			self.hspeed = 0
		self.get_keys()
		if self.ability_run >= 0:
			if self.ability_time > 0 or self.ability_time == -1:
				if self.ability_time > 0:
					self.ability_time -= self.game.dt
				exec(['self.run_special0()','self.run_special1()','self.run_special2()','self.run_special3()'][self.ability_run])
			else: self.atkEnd()
		else:self.hit_list = [self];self.freeze = 0
		if self.vspeed<0 and len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.x-self.hitbox[2]//2+1, self.y-self.hitbox[3]+self.vspeed*self.game.dt, self.hitbox[2]-2, 1) and x.platform==0]): self.vspeed=0
		self.y += self.vspeed * self.game.dt
		hit = bool(len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox[0]+self.hspeed*self.game.dt, self.y+4-72, 40, 68) and not x.platform]))
		if not hit or len(self.grounded):self.x+=self.hspeed*self.game.dt
		self.hitbox = (self.x+4-24,self.y+4-72,40,68)
		#Draw Character
		#pygame.draw.rect(self.game.win,(RED, GREEN, BLUE, YELLOW)[self.joystick.get_id()],(self.x-48/2,self.y-72,48,72))
		self.game.win.blit(self.sprite_image[0],(self.x-10.5,self.y-120))
		self.game.win.blit(self.sprite_image[1],(self.x-21,self.y-99))
		#self.game.win.blit(pygame.transform.rotate(self.sprite_image[2],90),(825,130))
		#self.game.win.blit(pygame.transform.rotate(self.sprite_image[3],90),(825,230))
		#self.game.win.blit(pygame.transform.rotate(self.sprite_image[4],-90),(975,130))
		#self.game.win.blit(pygame.transform.rotate(self.sprite_image[5],-90),(975,230))
		self.game.win.blit(self.sprite_image[2],(self.x-51,self.y-99))
		self.game.win.blit(self.sprite_image[3],(self.x-66,self.y-99))
		self.game.win.blit(self.sprite_image[4],(self.x+21,self.y-99))
		self.game.win.blit(self.sprite_image[5],(self.x+51,self.y-99))
		self.game.win.blit(self.sprite_image[6],(self.x-21,self.y-45))
		self.game.win.blit(self.sprite_image[7],(self.x-21,self.y-15))
		self.game.win.blit(self.sprite_image[8],(self.x+6,self.y-45))
		self.game.win.blit(self.sprite_image[9],(self.x+6,self.y-15))
		pygame.draw.rect(self.game.win, BLACK, self.hitbox,2)
		#######
		if self.y < 0:
			arrowX = max(min(self.x,RES[0]),0)
			pygame.draw.polygon(self.game.win,(RED, GREEN, BLUE, YELLOW)[self.joystick.get_id()],((arrowX,0),(arrowX-16,16),(arrowX+16,16)))
		else:
			if self.x > RES[0]:
				pygame.draw.polygon(self.game.win,(RED, GREEN, BLUE, YELLOW)[self.joystick.get_id()],((RES[0],self.y),(RES[0]-16,self.y+16),(RES[0]-16,self.y-16)))
			elif self.x < 0:
				pygame.draw.polygon(self.game.win,(RED, GREEN, BLUE, YELLOW)[self.joystick.get_id()],((0,self.y),(16,self.y+16),(16,self.y-16)))

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

	def atkHeavy(self,direction):
		exec(['self.special1(direction)','self.special1(direction)','self.special2()','self.special3()','self.special0()'][direction])

	def knockBack(self,hit,direction=0):
		#direction represents the direction of the attacking player
		self.ability_air=0
		self.gravityMultiplier=1
		Knockback_force = (((hit)**1.2) * ((self.dmg+30)**1.1))/10
		self.stun = min(int(Knockback_force/800),1.5)
		#print(Knockback_force,hit,self.stun)
		self.knocked = 1
		if direction < 2:
			self.hspeed = (direction-0.5)*2*Knockback_force*math.cos(math.pi/6) * (60/max(1,self.game.clock.get_fps()))
			self.vspeed = -Knockback_force*math.sin(math.pi/6) * (60/max(1,self.game.clock.get_fps()))
		elif direction >= 2:
			self.vspeed = ((direction==3)-0.5)*2*Knockback_force * (60/max(1,self.game.clock.get_fps()))
		self.currentJumps = max(1, self.currentJumps)
		#Don't remove the line below. It fixes the sliding bug
		self.y -= 5

	def atkEnd(self):
		if not(self.ability_time == -1):
			self.ability_time = 0
			self.ability_run = -1

	def damage(self, hit):
		self.dmg+=(hit*(1 - self.defense/20))

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
						self.release = 1

		else:
			self.stun -= self.game.dt


class Mage(Char):

	def special0(self):
		if not self.ability_run+1:
			self.release = 0
			self.special_0_timer = 0
			self.special_0_go = 0
			self.freeze=1
			self.ability_run = 0
			self.ability_time = -1
			self.explosion = self.game.effects['explosion'].copy()
			self.special_0_len = len(self.explosion)
			self.special_0_count = 0

	def run_special0(self):
		if self.release and not(self.special_0_count):
			self.special_0_go = 1
			scale = min(int(self.special_0_timer * 400 + 150),400)
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale,scale))
			self.LocNow = (self.x-((self.facing==0)*(scale+24-(scale/4)))+((self.facing==1)*(24-(scale/4)))+(64*(self.facing*2-1)),self.y-(scale))
			self.scale = scale
		else:
			self.special_0_timer += self.game.dt
			if self.special_0_timer > 1: self.release=1;
		if self.special_0_go:
			if self.special_0_count < self.special_0_len:
				self.game.win.blit(self.explosion[self.special_0_count],self.LocNow)
				if self.special_0_count <= 8:
					#Change the spawn location dependant on variable scale
					pygame.draw.rect(self.game.win,BLUE,(self.LocNow[0]+(self.scale/4),self.LocNow[1]+(self.scale/4),self.scale/2,3*self.scale/4),4)
					collisions=[(pygame.Rect((self.LocNow[0]+(self.scale/4),self.LocNow[1]+(self.scale/4),self.scale/2,3*self.scale/4)).colliderect(x.hitbox),x)for x in self.game.sprites]
				else: collisions = [];self.freeze=0
				self.special_0_count += 1
				[(x[1].knockBack((self.scale//10), self.facing),x[1].damage(self.scale//10))for x in collisions if x[0] and not(x[1] in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.ability_run = -1
				self.ability_time = 0
				self.release = 0



	def special1(self,direction):
		#sends a ball that explodes on release
		#Perhaps change to on impact and on repress since holding the key doesn't feel right
		if not self.ability_run+1:
			self.freeze = 1
			self.ability_run = 1
			self.ability_time = 0.2
			self.explosion = self.game.effects['ball_explosion'].copy()
			self.special_1_len = len(self.explosion)
			fireball(self,self.x-86,self.y-144,self.facing)
	def run_special1(self):pass

	def special2(self):
		if self.ability_run+1 == 0 and not(self.ability_air):
			self.ability_air = 1
			size = 175
			self.ability_run = 2
			self.ability_time = 0.3
			self.special_2_count = 0
			self.explosion = self.game.effects['boost_explosion'].copy()
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.flip(pygame.transform.scale(j,(size,size)),self.facing,1)
			self.LocNow = (self.x-size/2,self.y-size/2)
	def run_special2(self):
		#Add Flame effect and hit box around character
		self.vspeed = -800
		self.gravityMultiplier = 12
		if self.special_2_count < len(self.explosion*2):
			self.game.win.blit(self.explosion[self.special_2_count//2],self.LocNow)
			self.special_2_count += 1
		pygame.draw.rect(self.game.win,BLUE,(self.LocNow[0]+43.75,self.LocNow[1]+43.75,87.5,116.667),4)
		collisions=[(pygame.Rect((self.LocNow[0]+43.75,self.LocNow[1]+43.75,87.5,116.667)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(12, 3),x[1].damage(16))for x in collisions if x[0] and not(x[1] in self.hit_list)]
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
		if self.hit_list != [self]:self.ability_air = 0


	def special3(self):
		#Drop bomb? *
		#toss fireball? *
		#cause aoe explosion from self? ***
		#bring laser from sky? **
		#
		if not self.ability_run+1:
			self.release = 0
			self.special_3_timer = 0
			self.special_3_go = 0
			self.freeze=1
			self.ability_run = 3
			self.ability_time = -1
			self.explosion = self.game.effects['aoe_explosion'].copy()
			self.special_3_len = len(self.explosion)
			self.special_3_count = 0


	def run_special3(self):
		if self.release and not(self.special_3_count):
			self.special_3_go = 1
			scale = min(int(self.special_3_timer * 100 + 100),300)
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale*2,scale))
			self.LocNow = (self.x+(24-scale),self.y-(scale))
			self.scale = scale
		else:
			self.special_3_timer += self.game.dt
			if self.special_3_timer > 2: self.release=1;
		if self.special_3_go:
			if self.special_3_count < self.special_3_len*2:
				self.game.win.blit(self.explosion[self.special_3_count//2],self.LocNow)
				pygame.draw.rect(self.game.win,BLUE,(self.LocNow[0]+(self.scale/6),self.LocNow[1]+(self.scale/6),4*self.scale/3,3*self.scale/4),4)
				collisions=[(pygame.Rect((self.LocNow[0]+(self.scale/6),self.LocNow[1]+(self.scale/6),4*self.scale/3,3*self.scale/4)).colliderect(x.hitbox),x)for x in self.game.sprites]
				self.special_3_count += 1
				random_direction = randint(0,3)
				if random_direction == 2:
					random_direction = 3
				[(x[1].knockBack((self.scale//200), random_direction),x[1].damage(self.scale//100))for x in collisions if x[0]]
			else:
				self.ability_run = -1
				self.ability_time = 0
				self.release = 0
		pass

class fireball(pygame.sprite.Sprite):
	def __init__(self,char,x,y,direction):
		pygame.sprite.Sprite.__init__(self,char.game.objects)
		self.char = char
		self.loc = (x,y)
		self.dir = direction
		self.hitTarget = 0
		self.count = 0
		self.go = 0
		self.explosion = self.char.explosion
		self.hit_list = [self,char]
	def update(self):
		if self.hitTarget and not(self.count):
			self.go = 1
		elif not(self.count):
			self.loc = (self.loc[0] + (self.dir-0.5)*20,self.loc[1])
			collisions = [(pygame.Rect((self.loc[0]+85,self.loc[1]+85,30,30)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
			self.hitTarget = bool(len([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)]))
		if self.go:
			if self.count < self.char.special_1_len*2:
				self.char.game.win.blit(self.explosion[self.count//2],self.loc)
				if self.count < 8:
					pygame.draw.rect(self.char.game.win,BLUE,(self.loc[0]+50,self.loc[1]+50,100,100),4)
					collisions=[(pygame.Rect((self.loc[0]+50,self.loc[1]+50,100,100)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
				else: collisions=[]
				self.count += 1
				[x[1].damage(15)for x in collisions if x[0]and not(x[1]in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.kill()
		else:
			self.char.game.win.blit(self.explosion[self.count],self.loc)
		if self.loc[0] < -200 or self.loc[0] > 1280:
			self.kill()

