import pygame, math
from random import randint, uniform
from settings import *
from map import *
from projectiles import *

class Char(pygame.sprite.Sprite):
	def __init__(self,game,joystick,char,buttonmap=[0,1,2,3,4,5]):
		self.groups = game.sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.sprite_image = self.game.char_sprites[char][:-1]
		stats = eval(str(self.game.char_sprites[char][-1]))[-1]
		self.x = 200
		self.y = 200
		self.maxMoveSpeed = (stats[-1]/5)*200+200
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
		self.ability_air_side = 0
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
		self.width = 40
		self.height = 120
		self.hitbox = (self.x-self.width//2,self.y-self.height,self.width,self.height)

		#Stats
		self.defense = stats[-2]
		self.attack = 1+(stats[0]/22)
	def __repr__(self):return"ID"+str(self.joystick.get_id())
	def update(self,keys,events):
		self.keys = keys
		self.events = events
		self.grounded = sorted([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.x-self.hitbox[2]//2+1, self.y, self.hitbox[2]-2, 2)], key=lambda x:x.platform)
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
				self.ability_air_side = 0
				self.currentJumps = self.maxJumps
				if self.vspeed>0:self.vspeed=0
				self.y=self.grounded[0].rect[1]
				if len(self.grounded) and self.gravityMultiplier == 3 and not len([x for x in self.grounded if not x.platform]):
					self.y += self.grounded[0].rect[3] + self.grounded[0].speed * self.game.dt * (self.grounded[0].dir > 1)
				self.x += self.grounded[0].speed*((self.grounded[0].dir==0)*-1 + (self.grounded[0].dir==1))*self.game.dt
				self.y += self.grounded[0].speed*(self.grounded[0].dir==3)*self.game.dt
		else: self.vspeed += self.gravity * self.gravityMultiplier * (60/(self.game.clock.get_fps()+(60*(self.game.clock.get_fps()==0))))
		if (self.knocked and (self.y < -500 or self.x > 2080 or self.x < -800)) or self.y > 1000 : #respawn on death
			self.dmg = 0
			self.stun = 0
			self.ability_run = 0
			self.freeze = 0
			self.ability_time = 0
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
		hit=len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox[0]+self.hspeed*self.game.dt, self.hitbox[1]+self.vspeed*self.game.dt, self.width, self.height) and not x.platform and x not in self.grounded])
		if not hit:self.x+=self.hspeed*self.game.dt
		self.hitbox = (self.x-self.width//2,self.y-self.height,self.width,self.height)
#		self.hitbox = (self.x+4-24,self.y-120,40,120)

		#Draw Character
		#Character List index [head,torso,L_arm,L_hand,R_arm,R_hand,L_leg,L_foot,R_leg,R_foot,sprite_data]
		character_surface = pygame.surface.Surface((256, 256))
		character_surface.fill((192,192,192))
		#pygame.draw.rect(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(self.x-48/2,self.y-72,48,72))
		character_surface.blit(self.sprite_image[0],(128-10.5,256-120))
		character_surface.blit(self.sprite_image[1],(128-21,256-99))
		#character_surface.blit(pygame.transform.rotate(self.sprite_image[2],90),(825,130))
		#character_surface.blit(pygame.transform.rotate(self.sprite_image[3],90),(825,230))
		#character_surface.blit(pygame.transform.rotate(self.sprite_image[4],-90),(975,130))
		#character_surface.blit(pygame.transform.rotate(self.sprite_image[5],-90),(975,230))
		character_surface.blit(self.sprite_image[2],(128-51,256-99))
		character_surface.blit(self.sprite_image[3],(128-66,256-99))
		character_surface.blit(self.sprite_image[4],(128+21,256-99))
		character_surface.blit(self.sprite_image[5],(128+51,256-99))
		character_surface.blit(self.sprite_image[6],(128-21,256-45))
		character_surface.blit(self.sprite_image[7],(128-21,256-15))
		character_surface.blit(self.sprite_image[8],(128+6,256-45))
		character_surface.blit(self.sprite_image[9],(128+6,256-15))
		character_surface.set_colorkey((192,192,192))
#		pygame.draw.rect(self.game.win, BLACK, self.hitbox,2)

		if self.facing: self.game.win.blit(character_surface,(self.x-128,self.y-256))
		else: self.game.win.blit(pygame.transform.flip(character_surface,1,0),(self.x-128,self.y-256))

		#######
		head = pygame.Surface((self.sprite_image[0].get_width(), self.sprite_image[0].get_height()))
		head.blit(self.sprite_image[0].copy(),(0,0))
		head.set_colorkey(GRAEY)
		if (self.x < 0 or self.x > RES[0]) and self.y>0: #draw offscreen arrows
			if self.x > RES[0]:
				pygame.draw.polygon(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],((RES[0],self.y),(RES[0]-16,self.y+16),(RES[0]-16,self.y-16)))
				pygame.draw.circle(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(RES[0]-28,int(self.y)), 20)
				self.game.win.blit(head, (RES[0]-38, self.y-10))
			elif self.x < 0:
				pygame.draw.polygon(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],((0,self.y),(16,self.y+16),(16,self.y-16)))
				pygame.draw.circle(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(28,int(self.y)), 20)
				self.game.win.blit(head, (18, self.y-10))
		elif self.y<0:
			arrowX = int(max(min(self.x,RES[0]-20),20))
			pygame.draw.polygon(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],((arrowX,0),(arrowX-16,16),(arrowX+16,16)))
			pygame.draw.circle(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(arrowX,28), 20)
			self.game.win.blit(head, (arrowX-10, 20))
		elif self.x < 0:
			pass
		elif self.x > RES[0]:
			pass

	def jump(self):
		if self.currentJumps:
			self.currentJumps -= 1
			self.vspeed = self.jumpSpeed
			self.jumpBonus = 0

	def atkLight(self, direction):
		if direction == 4:
			direction = self.facing
		if direction < 2:
			pygame.draw.rect(self.game.win,BLUE,(self.x-self.width+((direction==1)*(self.width+20)), self.y-self.height, 20, self.height),4)
			collisions=[(pygame.Rect((self.x-self.width+((direction==1)*(self.width+20)),self.y-self.height,20,self.height)).colliderect(x.hitbox),x)for x in self.game.sprites]
		elif direction >= 2:
			pygame.draw.rect(self.game.win,BLUE,(self.x-self.width//2,20+self.y-(self.height+30)+((direction==3)*(self.height+10)),self.width,30),4)
			collisions=[(pygame.Rect((self.x-self.width//2,20+self.y-(self.height+30)+((direction==3)*(self.height+10)),self.width,30)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(6*self.attack, direction),x[1].damage(5*self.attack))for x in collisions if x[0] and x[1]!=self]

	def atkHeavy(self,direction):
		try:exec(['self.special1(direction)','self.special1(direction)','self.special2()','self.special3()','self.special0()'][direction])
		except Exception as e:print(e)

	def knockBack(self,hit,direction=0):
		#direction represents the direction of the attacking player
		self.ability_air=0
		self.gravityMultiplier=1
		Knockback_force = ((((hit)**1.2) * ((self.dmg+30)**1.1))/10)*(1.5-((self.defense-1)/10))
		self.stun = min(int(Knockback_force/4000),1.5)
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
			Slow_multiplier = (abs((self.freeze==0)-0.2)+0.2) * (((self.freeze==2)-1)*-1)
			if  self.joystick.get_axis(0) < -.5 and self.freeze!=2:
				self.hspeed = max(self.hspeed-self.moveSpeed*(60/max(1,self.game.clock.get_fps())), -self.maxMoveSpeed) * Slow_multiplier
				self.facing = 0
			elif self.joystick.get_axis(0) > .5 and self.freeze!=2:
				self.hspeed = min(self.hspeed+self.moveSpeed*(60/max(1,self.game.clock.get_fps())), self.maxMoveSpeed) * Slow_multiplier
				self.facing = 1
			elif self.hspeed and not(self.knocked):
				if abs(self.hspeed)>self.moveSpeed: self.hspeed -= (self.hspeed/abs(self.hspeed) * self.moveSpeed * (bool(not self.grounded)*.15 + bool(self.grounded)) * (60/max(1,self.game.clock.get_fps())))/((self.grounded==0)*5+1)
				else: self.hspeed = 0
			self.gravityMultiplier = (self.joystick.get_axis(1) >.9)*2 + 1
			if self.joystick.get_button(self.buttonmap[0]) and (self.vspeed < 0) and (self.jumpBonus < self.maxJumpBonus):
				self.vspeed += self.jumpBonusSpeed * (60/max(1,self.game.clock.get_fps()))
				self.jumpBonus += 1
			for e in self.events:
				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:self.knockBack(60*self.attack,self.facing) #testing only, remove later
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
			self.LocNow = (self.x-((self.facing==0)*(scale+self.width//2-(scale/4)))+((self.facing==1)*(self.width//2-(scale/4)))+(64*(self.facing*2-1)),self.y-(scale))
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
				[(x[1].knockBack((self.scale//10)*self.attack, self.facing),x[1].damage(self.scale//10 * self.attack))for x in collisions if x[0] and not(x[1] in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.ability_run = -1
				self.ability_time = 0
				self.release = 0



	def special1(self,direction):
		#sends a ball that explodes on release
		#Perhaps change to on impact and on repress since holding the key doesn't feel right
		if not self.ability_run+1:
			self.freeze = 2
			self.ability_run = 1
			self.ability_time = 0.2
			self.explosion = self.game.effects['ball_explosion'].copy()
			self.special_1_len = len(self.explosion)
			fireball(self,self.x-86,self.y-184,self.facing)
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
		[(x[1].knockBack(12*self.attack, 3),x[1].damage(16 * self.attack))for x in collisions if x[0] and not(x[1] in self.hit_list)]
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
			self.LocNow = (self.x+(self.width//2-scale),self.y-(scale))
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
				[(exec("x[1].knockBack((self.scale//20)*self.attack, x[1].x>(self.LocNow[0]+self.scale))"*(x[1]!=self)),x[1].damage(self.scale//100 * self.attack))for x in collisions if x[0]]
			else:
				self.ability_run = -1
				self.ability_time = 0
				self.release = 0
		pass

class друг(Char):
	def special0(self):
		if not self.ability_run+1:
			self.ability_run = 0
			self.release = 0
			self.freeze = 2
			self.ability_time = -1
			self.fire = self.game.effects['flaming_turds'].copy()
			self.special_0_len = len(self.fire)
			self.ability_count = -8
	def run_special0(self):
		if self.release or (self.ability_count>0): self.ability_run=-1;self.release=0
		self.ability_count += .2
		rainbow_poop(self,self.x,self.y-40,self.facing, yspeed=self.ability_count, xspeed=(-self.ability_count+10)/20)

	def special1(self, dir):
		if not (self.ability_run+1 or self.ability_air_side):
			self.ability_air_side = 1
			self.freeze=2
			self.fire = self.game.effects['flaming_turds'].copy()
			self.ability_run = 1
			self.ability_time = 0.3
	def run_special1(self):
		self.hspeed = 1200*(self.facing*2-1)
		self.vspeed = 0
		self.gravityMultiplier = 0
		rainbow_poop(self,self.x,self.y-40,not self.facing,yspeed=uniform(-4,4),xspeed=uniform(1,2))
		collisions=[(pygame.Rect(self.hitbox).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(14*self.attack, self.facing),x[1].damage(5*self.attack))for x in collisions if x[0] and not(x[1] in self.hit_list)]
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])


	def special2(self):
		self.ability_air_side = 0
		if self.ability_run+1 == 0 and not(self.ability_air):
			self.ability_air = 1
			self.fire = self.game.effects['flaming_turds'].copy()
			self.ability_run = 2
			self.ability_time = 0.3
	def run_special2(self):
		self.vspeed = -800
		self.gravityMultiplier = 12
		[rainbow_poop(self,self.x,self.y-40,randint(0,1),yspeed=5,xspeed=uniform(0,.25),bounce=1)for x in".."]

