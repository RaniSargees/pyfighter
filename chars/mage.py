import pygame
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not self.ability_run+1:
			self.release = 0
			self.special_0_timer = 0
			self.special_0_go = 0
			self.freeze=1
			self.ability_run = 0
			self.ability_time = -1
			self.explosion = self.game.effects['explosion'].copy()
			self.charging = self.game.effects['charging'].copy()
			self.special_0_len = len(self.explosion)
			self.special_0_count = 0
			self.frame_count = 0

	def run_special0(self):
		if self.release and not(self.special_0_count):
			self.special_0_go = 1
			self.game.Sounds.play('explosion')
			scale = min(int(self.special_0_timer * 400 + 150),400)
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale,scale))
			self.LocNow = (self.x-((self.facing==0)*(scale+self.width//2-(scale/4)))+((self.facing==1)*(self.width//2-(scale/4)))+(64*(self.facing*2-1)),self.y-(scale))
			self.scale = scale
		else:
			if not(self.special_0_go):
				self.game.win.blit(pygame.transform.scale(self.charging[self.frame_count%98],(50,50)),(self.x-25+(self.facing-0.5)*250,self.y-80))
				self.frame_count += 1
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
			self.game.Sounds.play('explosion')
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
			self.charging = self.game.effects['charging'].copy()
			self.special_3_len = len(self.explosion)
			self.special_3_count = 0
			self.frame_count = 0


	def run_special3(self):
		if self.release and not(self.special_3_count):
			self.game.Sounds.play('explosion')
			self.special_3_go = 1
			scale = min(int(self.special_3_timer * 100 + 100),300)
			for i,j in enumerate(self.explosion):self.explosion[i]=pygame.transform.scale(j,(scale*2,scale))
			self.LocNow = (self.x+(self.width//2-scale),self.y-(scale))
			self.scale = scale
		else:
			if not(self.special_3_go):
				self.img.append((pygame.transform.scale(self.charging[self.frame_count%98],(20+self.frame_count,20+self.frame_count)),(self.x-(10+(self.frame_count/2)),self.y-(20+self.frame_count))))
				self.frame_count += 1
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

