import pygame
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not self.ability_run+1:#Don't run ability if there is another one running
			self.release = 0#Sets up init variables for ability
			self.special_0_timer = 0
			self.special_0_go = 0
			self.freeze=1
			self.ability_run = 0
			self.ability_time = -1
			self.explosion = self.game.effects['explosion'].copy()#Loads in animations
			self.charging = self.game.effects['charging'].copy()
			self.special_0_len = len(self.explosion)
			self.special_0_count = 0
			self.frame_count = 0

	def run_special0(self):
		if self.release and not(self.special_0_count):#Waits until the special button is released
			self.special_0_go = 1#
			self.game.Sounds.play('explosion')
			scale = min(int(self.special_0_timer * 400 + 150),400)#Determine explosion size dependent on charging time
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale,scale))
			self.LocNow = (self.x-((self.facing==0)*(scale+self.width//2-(scale/4)))+((self.facing==1)*(self.width//2-(scale/4)))+(64*(self.facing*2-1)),self.y-(scale))
			self.scale = scale
		else:#If the special button is still pressed play charging animation and increase counter
			if not(self.special_0_go):
				self.game.win.blit(pygame.transform.scale(self.charging[self.frame_count%98],(50,50)),(self.x-25+(self.facing-0.5)*250,self.y-80))
				self.frame_count += 1
			self.special_0_timer += self.game.dt
			if self.special_0_timer > 1: self.release=1;#Max charging time is 1 second
		if self.special_0_go:#Start ability
			if self.special_0_count < self.special_0_len:#Play explosion animation
				self.game.win.blit(self.explosion[self.special_0_count],self.LocNow)
				if self.special_0_count <= 8:
					#Change the spawn location dependent on variable scale and calculate collisions
					collisions=[(pygame.Rect((self.LocNow[0]+(self.scale/4),self.LocNow[1]+(self.scale/4),self.scale/2,3*self.scale/4)).colliderect(x.hitbox),x)for x in self.game.sprites]
				else: collisions = [];self.freeze=0
				self.special_0_count += 1
				#Calculate knock back and damage dealt to players explosion has collided with
				[(x[1].knockBack((self.scale//10)*self.attack, self.facing),x[1].damage(self.scale//10 * self.attack))for x in collisions if x[0] and not(x[1] in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])#Add all players hit into list such that they can't be hit again with same ability
			else:
				#Reset variables and turn off ability
				self.ability_run = -1
				self.ability_time = 0
				self.release = 0



	def special1(self,direction):
		#sends a ball that explodes on impact
		if not self.ability_run+1:
			self.freeze = 2#Init variables
			self.ability_run = 1
			self.ability_time = 0.2
			self.explosion = self.game.effects['ball_explosion'].copy()
			self.special_1_len = len(self.explosion)
			fireball(self,self.x-86,self.y-184,self.facing)#Creates fireball object
	def run_special1(self):pass

	def special2(self):
		if self.ability_run+1 == 0 and not(self.ability_air):
			self.game.Sounds.play('explosion')#init variables
			self.ability_air = 1
			size = 175
			self.ability_run = 2
			self.ability_time = 0.3
			self.special_2_count = 0
			self.explosion = self.game.effects['boost_explosion'].copy()
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.flip(pygame.transform.scale(j,(size,size)),self.facing,1)#Reverses effect if player is facing right
			self.LocNow = (self.x-size/2,self.y-size/2)
	def run_special2(self):
		self.vspeed = -800#Shoots player upwards
		self.gravityMultiplier = 12#Increases player gravity
		if self.special_2_count < len(self.explosion*2):#Plays animation
			self.game.win.blit(self.explosion[self.special_2_count//2],self.LocNow)
			self.special_2_count += 1
		collisions=[(pygame.Rect((self.LocNow[0]+43.75,self.LocNow[1]+43.75,87.5,116.667)).colliderect(x.hitbox),x)for x in self.game.sprites]#Tests for collisions with other players
		[(x[1].knockBack(12*self.attack, 3),x[1].damage(16 * self.attack))for x in collisions if x[0] and not(x[1] in self.hit_list)]#Deals damage and knock back to them if they did collide
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])#prevents players from being hit twice with the same ability
		if self.hit_list != [self]:self.ability_air = 0#Adds another use of the ability in midair if you a player using this


	def special3(self):
		if not self.ability_run+1:
			self.release = 0#init variables
			self.special_3_timer = 0
			self.special_3_go = 0
			self.freeze=1
			self.ability_run = 3
			self.ability_time = -1
			self.explosion = self.game.effects['aoe_explosion'].copy()#Loads in animations
			self.charging = self.game.effects['charging'].copy()
			self.special_3_len = len(self.explosion)
			self.special_3_count = 0
			self.frame_count = 0


	def run_special3(self):
		if self.release and not(self.special_3_count):#calculate effect size and damage once special button is released
			self.game.Sounds.play('explosion')
			self.special_3_go = 1
			scale = min(int(self.special_3_timer * 100 + 100),300)
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale*2,scale))
			self.LocNow = (self.x+(self.width//2-scale),self.y-(scale))
			self.scale = scale
		else:#Charging time and animation
			if not(self.special_3_go):
				self.img.append((pygame.transform.scale(self.charging[self.frame_count%98],(20+self.frame_count,20+self.frame_count)),(self.x-(10+(self.frame_count/2)),self.y-(20+self.frame_count))))
				self.frame_count += 1
			self.special_3_timer += self.game.dt
			if self.special_3_timer > 2: self.release=1;#max charging time is 2 seconds
		if self.special_3_go:
			if self.special_3_count < self.special_3_len*2:#Plays explosion animation
				self.game.win.blit(self.explosion[self.special_3_count//2],self.LocNow)
				#test who got hit
				collisions=[(pygame.Rect((self.LocNow[0]+(self.scale/6),self.LocNow[1]+(self.scale/6),4*self.scale/3,3*self.scale/4)).colliderect(x.hitbox),x)for x in self.game.sprites]
				self.special_3_count += 1
				#Calculates damage and knock back for players hit (including the casting player) and deals damage and knock back. (no knock back for casting player only damage) 
				[(exec("x[1].knockBack((self.scale//20)*self.attack, x[1].x>(self.LocNow[0]+self.scale))"*(x[1]!=self)),x[1].damage(self.scale//100 * self.attack))for x in collisions if x[0]]
			else:#Reset variables
				self.ability_run = -1
				self.ability_time = 0
				self.release = 0
		pass

