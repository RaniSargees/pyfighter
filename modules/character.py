import pygame, math
from random import randint, uniform
from settings import *
from modules.map import *
from modules.projectiles import *
from modules.animation import *

class Char(pygame.sprite.Sprite):
	def __init__(self,game,joystick,char,buttonmap=[0,1,2,3,4,5]):
		self.groups = game.sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.sprite_image = self.game.char_sprites[char][:-1]
		self.anim = animator(self.sprite_image)
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
#		self.inStage = 0
		self.hit_list = [self]
		self.ability_time = 0
		self.ability_air = 0
		self.ability_air_side = 0
		self.ability_run = -1
		self.ability_delay_time = 0
		self.release = 0
		self.dmg = 0
		self.stun = 0
		self.BTNDown = 0
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
#		self.inStage = False
		self.ability_delay_time -= self.game.dt
		if self.ability_delay_time < 0:
			self.ability_delay_time = 0
#		for i in self.grounded:
#			self.inStage = (self.x <= (i.rect[0]+i.rect[2]) and self.x >= i.rect[0])
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

		#Draw Character
		#Character List index [head,torso,L_arm,L_hand,R_arm,R_hand,L_leg,L_foot,R_leg,R_foot,sprite_data]
		attacking = 0 #TODO add a real check here
		if not attacking:
			if self.hspeed and self.grounded:character_surface = self.anim.walk(self.hspeed)
			elif not self.hspeed and self.grounded:character_surface = self.anim.idle()
			else:character_surface = self.anim.jump()
		else:
			pass #TODO add attack animations
		if self.facing: self.game.win.blit(character_surface,(self.x-128,self.y-256))
		else: self.game.win.blit(pygame.transform.flip(character_surface,1,0),(self.x-128,self.y-256))

		if self.ability_run >= 0:
			if self.ability_time > 0 or self.ability_time == -1:
				if self.ability_time > 0:
					self.ability_time -= self.game.dt
				exec(['self.run_special0()','self.run_special1()','self.run_special2()','self.run_special3()'][self.ability_run])
			else: self.atkEnd()
		else:
			self.hit_list = [self]
			if self.freeze != 3:
				self.freeze = 0
		if self.vspeed<0 and len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.x-self.hitbox[2]//2+1, self.y-self.hitbox[3]+self.vspeed*self.game.dt, self.hitbox[2]-2, 1) and x.platform==0]): self.vspeed=0
		self.y += self.vspeed * self.game.dt
		while 1:
			if not len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox[0]+self.hspeed*self.game.dt, self.hitbox[1]+self.vspeed*self.game.dt, self.width, self.height) and not x.platform and x not in self.grounded]):break
			self.hspeed = int(self.hspeed/2)
			if not self.hspeed: break
		self.x+=self.hspeed*self.game.dt
		self.hitbox = (self.x-self.width//2,self.y-self.height,self.width,self.height)
#		self.hitbox = (self.x+4-24,self.y-120,40,120)


#		pygame.draw.rect(self.game.win, BLACK, self.hitbox,2)



		#######
		head = self.sprite_image[0].copy()
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
		if self.currentJumps and self.freeze != 3:
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
		try: [exec('x.freeze=0') for x in self.target]
		except: pass
		self.ability_run = -1
		self.ability_time = 0
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
			Slow_multiplier = (abs((self.freeze==0)-0.2)+0.2) * (((self.freeze==2 or self.freeze==3)-1)*-1)
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
					self.BTNDown = 1
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
					self.BTNDown = 0
					if e.button == self.buttonmap[1]:
						self.release = 1

		else:
			self.stun -= self.game.dt



