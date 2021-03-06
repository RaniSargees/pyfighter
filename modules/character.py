#			Character
#Base class for all character objects
#Use WASD or joystick to control character
#J_keyboard or X_controller(xBOX) for a light attack
#K_keyboard or B_controller(xBOX) for a heavy attack
#Space_Keyboard or A_controller(xBOX) for a jump


import pygame, math
from random import randint, uniform
from settings import *
from modules.map import *
from modules.projectiles import *
from modules.animation import *
from time import time

class Char(pygame.sprite.Sprite):
	def __init__(self,game,joystick,char,buttonmap=[0,1,2,3,4,5]):
		self.groups = game.sprites #store group
		pygame.sprite.Sprite.__init__(self, self.groups) #init self as sprite in group
		self.game = game #store game
		self.name = char #store character name
		self.sprite_image = self.game.char_sprites[char][:-1] #store sprite images
		self.anim = animator(self.sprite_image) #setup animator class
		self.obj_name = eval(str(self.game.char_sprites[char][-1]))[0]
		stats = eval(str(self.game.char_sprites[char][-1]))[-1] #setup stats
		self.x = 200 #setup starting position (overriden by spawn platform)
		self.y = 200
		self.maxMoveSpeed = (stats[-1]/5)*200+200 #setup maximum move speed using stats
		self.moveSpeed = 60 #accelleration, not changed
		self.jumpSpeed = -500 #jump height
		self.jumpBonusSpeed = -30 #additional jump height granted per frame of holding jump button
		self.maxJumps = 2 #allow double jumping
		self.jumpBonus = 0 #jump bonus variables
		self.maxJumpBonus = 10
		self.currentJumps = self.maxJumps #jumps remaining
		self.vspeed = 0 #vertical speed
		self.hspeed = 0 #horizontal speed
		self.gravity = 32 #added to y value every frame
		self.stock = 4 #start with 4 lives
		self.dead = 0 #not dead
		self.gravityMultiplier = 1 #used for fast fall and falling through platforms
		self.joystick = joystick #save joystick
		self.buttonmap = buttonmap #save joystick remapping
		self.spawning = 0 #used to control spawn platforms
		self.hit_list = [self] #stores players to not hit with attacks
		self.ability_time = 0 #variables controlling special abilities
		self.ability_air = 0
		self.ability_air_side = 0
		self.ability_run = -1
		self.ability_delay_time = 0
		self.release = 0
		self.dmg = 0 #current amount of damage
		self.img = [] #used by special abilities to draw images on top of character instead of behind
		self.stun = 0 #stun character after attacks
		self.BTNDown = 0 #controls charging heavy attacks
		self.knocked = 0 #whether character was knocked back or jumped from ground
		self.freeze = 0 #freeze during special attacks
		self.facing = 0 #store facing left/right for sprite flipping
		#0 = Left
		#1 = Right
		#2 = Up
		#3 = Down
		self.width = 40 #hitbox calculations
		self.height = 120
		self.hitbox = (self.x-self.width//2,self.y-self.height,self.width,self.height)
		self.latktimer = 0 #used to control animation of light attacks
		self.latkdir = 0
		#Stats
		self.defense = stats[-2]
		self.attack = 1+(stats[0]/22)
		self.respawn() #start self on spawn platform
	def __repr__(self):return"ID"+str(self.joystick.get_id()) #return player ID
	def update(self,keys,events):
		if self.dead: #quit if dead
			return 1
		self.keys = keys #save keys and events
		self.events = events
		#store ground objects character is standing on
		self.grounded = sorted([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.x-self.hitbox[2]//2+1, self.y, self.hitbox[2]-2, 2)], key=lambda x:x.platform)
		self.ability_delay_time -= self.game.dt #control ability delays
		if self.ability_delay_time < 0:
			self.ability_delay_time = 0
		if self.grounded: #if standing on the ground
			if self.stun <= 0: #reset knockback
				self.knocked = 0
			if self.spawning: #set spawning to 0
				self.spawning -= self.game.dt
				if self.spawning < 0:
					self.spawning = 0
			if self.knocked: #if knocked back
				if self.grounded[0].platform==0: #slow self if on ground platform
					self.hspeed *= 0.1
					self.vspeed *= -1
					self.stun = 0
			else:
				self.ability_air = 0 #reset air special abilities
				self.ability_air_side = 0
				self.currentJumps = self.maxJumps #reset jumps
				if self.vspeed>0:self.vspeed=0 #stop falling
				self.y=self.grounded[0].rect[1] #jump to top of ground object
				if len(self.grounded) and self.gravityMultiplier == 3 and not len([x for x in self.grounded if not x.platform]): #Fall through platforms when Down key is pressed
					self.y += self.grounded[0].rect[3] + self.grounded[0].speed * self.game.dt * (self.grounded[0].dir > 1)
				self.x += self.grounded[0].speed*((self.grounded[0].dir==0)*-1 + (self.grounded[0].dir==1))*self.game.dt #if platform is moving¸ move with it
				self.y += self.grounded[0].speed*(self.grounded[0].dir==3)*self.game.dt
		else: self.vspeed += self.gravity * self.gravityMultiplier * (60/(self.game.clock.get_fps()+(60*(self.game.clock.get_fps()==0)))) #add gravity if in air
		if (self.knocked and (self.y < -500 or self.x > 2080 or self.x < -800)) or self.y > 1000 : #respawn on death
			self.stock -= 1
			self.respawn()
		self.get_keys() #get joystick presses / do attacks and jumps
		if self.ability_run >= 0: #if set to run ability
			if self.ability_time > 0 or self.ability_time == -1: #check if ability is still running
				if self.ability_time > 0:
					self.ability_time -= self.game.dt #decrease ability time if ability is time limited
				if   self.ability_run==0:character_surface=self.run_special0() #run special update method
				elif self.ability_run==1:character_surface=self.run_special1()
				elif self.ability_run==2:character_surface=self.run_special2()
				elif self.ability_run==3:character_surface=self.run_special3()
				if character_surface == None: character_surface = self.anim.idle() #idle if the ability doesnt set an animation
			else: self.atkEnd();character_surface=self.anim.idle() #end attack, idle
		else: #reset variables for special attacks when none ar running
			self.hit_list = [self]
			if self.freeze != 3:
				self.freeze = 0
			if self.latktimer:character_surface=self.anim.punch(self.latkdir) #run animations (walk, idle, punch)
			elif self.hspeed and self.grounded:character_surface = self.anim.walk(self.hspeed)
			#elif not self.hspeed and self.grounded:
			else:character_surface = self.anim.idle()
#			else:character_surface = self.anim.jump() # this animation sucks, just leave it commented

		#Draw Character
		#Character List index [head,torso,L_arm,L_hand,R_arm,R_hand,L_leg,L_foot,R_leg,R_foot,sprite_data]
		#Character list is now deprecated, use animator
		if self.facing: self.game.win.blit(character_surface,(self.x-128,self.y-256)) #draw surface flipped for facing direction
		else: self.game.win.blit(pygame.transform.flip(character_surface,1,0),(self.x-128,self.y-256))

		if self.latktimer:self.latktimer-=1 #lower light attack timer (used only for animation, light attack only really lasts 1 frame)
		for i in self.img: #For blitting stuff after the character
			self.game.win.blit(i[0],i[1])
		self.img = []
		#stop moving if moving upwards and game ground above
		if self.vspeed<0 and len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.x-self.hitbox[2]//2+1, self.y-self.hitbox[3]+self.vspeed*self.game.dt, self.hitbox[2]-2, 1) and x.platform==0]): self.vspeed=0
		self.y += self.vspeed * self.game.dt #add vspeed per frame with delta time
		while 1: #lower horizontal speed until no longer clipping into a wall
			if not len([x for x in self.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox[0]+self.hspeed*self.game.dt, self.hitbox[1]+self.vspeed*self.game.dt, self.width, self.height) and not x.platform and x not in self.grounded]):break
			self.hspeed = int(self.hspeed/2)
			if not self.hspeed: break
		self.x+=self.hspeed*self.game.dt #add horizontal speed per frame with delta time
		self.hitbox = (self.x-self.width//2,self.y-self.height,self.width,self.height) #re-generate hitbox

		#######
		head = self.sprite_image[0].copy()
		if (self.x < 0 or self.x > RES[0]) and self.y>0 and not(self.spawning): #draw offscreen arrows
			if self.x > RES[0]:
				pygame.draw.polygon(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],((RES[0],self.y),(RES[0]-16,self.y+16),(RES[0]-16,self.y-16)))
				pygame.draw.circle(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(RES[0]-28,int(self.y)), 20)
				self.game.win.blit(head, (RES[0]-38, self.y-10))
			elif self.x < 0:
				pygame.draw.polygon(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],((0,self.y),(16,self.y+16),(16,self.y-16)))
				pygame.draw.circle(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(28,int(self.y)), 20)
				self.game.win.blit(head, (18, self.y-10))
		elif self.y<0 and not(self.spawning):
			arrowX = int(max(min(self.x,RES[0]-20),20))
			pygame.draw.polygon(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],((arrowX,0),(arrowX-16,16),(arrowX+16,16)))
			pygame.draw.circle(self.game.win,(BLUE, RED, YELLOW, GREEN)[self.joystick.get_id()],(arrowX,28), 20)
			self.game.win.blit(head, (arrowX-10, 20))
		elif self.x < 0: #was going to be used for corner arrows, unimplemented
			pass
		elif self.x > RES[0]:
			pass

	def jump(self): #jump
		if self.currentJumps and self.freeze != 3 and self.freeze != 2:
			self.currentJumps -= 1 #lower jump count
			self.vspeed = self.jumpSpeed #jump
			self.jumpBonus = 0 #reset bonus, added by get_keys

	def atkLight(self, direction): #punch in some direction
		if not self.latktimer:
			self.latkdir=direction #set animation variables
			self.latktimer=8
			if direction == 4: #punch
				direction = self.facing
			if direction < 2:
				collisions=[(pygame.Rect((self.x-self.width+((direction==1)*(self.width+50))-30,self.y-self.height,50,self.height)).colliderect(x.hitbox),x)for x in self.game.sprites]
			elif direction >= 2:
				collisions=[(pygame.Rect((self.x-self.width//2,20+self.y-(self.height+30)+((direction==3)*(self.height+10)),self.width,30)).colliderect(x.hitbox),x)for x in self.game.sprites]
			[(x[1].knockBack(6*self.attack, direction),x[1].damage(5*self.attack))for x in collisions if x[0] and x[1]!=self]

	def atkHeavy(self,direction): #Starts special/heavy attack
		try:exec(['self.special1(direction)','self.special1(direction)','self.special2()','self.special3()','self.special0()'][direction])
		except Exception as e:print(e)

	def knockBack(self,hit,direction=0):
		#direction represents the direction of the attacking player
		try: [exec('x.freeze=0') for x in self.target]
		except: pass
		self.game.Sounds.play('oof') #oof.
		self.ability_run = -1 #reset ability variables
		self.ability_time = 0
		self.ability_air=0
		self.gravityMultiplier=1 #reset gravty
		Knockback_force = ((((hit)**1.2) * ((self.dmg+30)**1.1))/10)*(1.5-((self.defense-1)/10)) #calculate knockback force
		self.stun = min(Knockback_force/4000,1.5) #calculate stun value
		self.knocked = 1 #set knockback var
		if direction < 2: #knock back player in direction
			self.hspeed = (direction-0.5)*2*Knockback_force*math.cos(math.pi/6) * (60/max(1,self.game.clock.get_fps()))
			self.vspeed = -Knockback_force*math.sin(math.pi/6) * (60/max(1,self.game.clock.get_fps()))
		elif direction >= 2:
			self.vspeed = ((direction==3)-0.5)*2*Knockback_force * (60/max(1,self.game.clock.get_fps()))
		self.currentJumps = max(1, self.currentJumps)
		#Don't remove the line below. It fixes the sliding bug
		#allows characters to be knocked upwards while on the ground, since ground would reset vspeed on collision
		self.y -= 5


	def atkEnd(self): #Resets attacking variables
		if not(self.ability_time == -1):
			self.ability_time = 0
			self.ability_run = -1

	def damage(self, hit): #Calculated damage
		self.dmg+=(hit*(1 - self.defense/20))

	def get_keys(self): #Does things when controller keys are pressed
		if self.stun <= 0 and not(self.spawning):
			Slow_multiplier = (abs((self.freeze==0)-0.2)+0.2) * (((self.freeze==2 or self.freeze==3)-1)*-1)
			if  self.joystick.get_axis(0) < -.5 and self.freeze!=2: #move left/right
				self.hspeed = max(self.hspeed-self.moveSpeed*(60/max(1,self.game.clock.get_fps())), -self.maxMoveSpeed) * Slow_multiplier
				self.facing = 0
			elif self.joystick.get_axis(0) > .5 and self.freeze!=2:
				self.hspeed = min(self.hspeed+self.moveSpeed*(60/max(1,self.game.clock.get_fps())), self.maxMoveSpeed) * Slow_multiplier
				self.facing = 1
			elif self.hspeed and not(self.knocked): #slow down if not moving or knocked
				if abs(self.hspeed)>self.moveSpeed: self.hspeed -= (self.hspeed/abs(self.hspeed) * self.moveSpeed * (bool(not self.grounded)*.15 + bool(self.grounded)) * (60/max(1,self.game.clock.get_fps())))/((self.grounded==0)*5+1)
				else: self.hspeed = 0
			self.gravityMultiplier = ((self.joystick.get_axis(1) >.9)*2*(self.freeze != 2) + 1) #increase gravity when joystick held down
			if self.joystick.get_button(self.buttonmap[0]) and (self.vspeed < 0) and (self.jumpBonus < self.maxJumpBonus): #add jump boost when already jumping
				self.vspeed += self.jumpBonusSpeed * (60/max(1,self.game.clock.get_fps()))
				self.jumpBonus += 1
			for e in self.events: #loop through events
#whoops, that was left in
#				if e.type == pygame.KEYDOWN and e.key == pygame.K_p:self.knockBack(60*self.attack,self.facing) #testing only, remove later
				if e.type == pygame.JOYBUTTONDOWN and e.joy==self.joystick.get_id(): #get events only for character joystick
					if e.button == self.buttonmap[0]: self.jump() #jump
					if e.button == self.buttonmap[2]:
						if self.joystick.get_axis(1)> .5: self.atkLight(3) #light attack
						elif self.joystick.get_axis(1)<-.5: self.atkLight(2)
						elif abs(self.joystick.get_axis(0))>.5: self.atkLight(self.facing)
						else: self.atkLight(4)
					elif e.button == self.buttonmap[1]: #heavy attack
						self.BTNDown = 1
						if self.joystick.get_axis(1)> .5: self.atkHeavy(3)
						elif self.joystick.get_axis(1)<-.5: self.atkHeavy(2)
						elif abs(self.joystick.get_axis(0))>.5: self.atkHeavy(self.facing)
						else: self.atkHeavy(4)
				elif e.type == pygame.JOYBUTTONUP and e.joy==self.joystick.get_id(): #release button for charged heavy attacks
					if e.button == self.buttonmap[1]:
						self.BTNDown = 0
						self.release = 1

		else:
			self.stun -= self.game.dt

	def respawn(self): #check if lives left, come down from top on spawn platform
		if self.stock: #reset variables
			self.spawning = 3
			self.ability_time = 0
			self.ability_air = 0
			self.ability_air_side = 0
			self.ability_run = -1
			self.ability_delay_time = 0
			self.gravityMultiplier = 1
			self.release = 0
			self.dmg = 0
			self.stun = 0
			self.BTNDown = 0
			self.knocked = 0
			self.freeze = 0
			self.facing = 0
			i = self.joystick.get_id()
			self.x = (96*(i+1)+(200*i)+100) #calculate X position
			self.y = -500 #spawn outside map
			self.vspeed = 0
			self.hspeed = 0
			TimedGround(self.game,(96*(i+1)+(200*i)+50,-500,100,20),3,200,200,7,texture = self.game.platform) #create timed platform to stand on
		else:
			self.dead = time() #store time of death in unix time (breaks if game played before jan 1 1970 or after jan 19 2038 on 32 bit systems)
