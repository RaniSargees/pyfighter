import pygame
from colorsys import hls_to_rgb
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
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
	
	def special3(self):
		if not(self.ability_run+1):
			self.release = 0
			self.ability_run = 3
			self.ability_time = -1
			self.hspeed = 0
			self.freeze = 2
			self.count = 0
			self.hue = 0
	
	def run_special3(self):
		self.color = [int(x*255) for x in hls_to_rgb(self.hue%360,0.5,1)]
		print(hls_to_rgb(self.hue%360,0.5,1))
		self.hue+=3
		pygame.draw.polygon(self.game.win,self.color,((self.x-7,self.y-79),(self.x-10,self.y-72),(self.x-7,self.y-65),(self.x+7,self.y-65),(self.x+10,self.y-72),(self.x+7,self.y-79)))
		
		
		if self.release:
			self.ability_run = 0
			self.ability_time = 0
			self.stun = 0.4
		

