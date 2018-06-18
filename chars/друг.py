import pygame
from random import random
from colorsys import hls_to_rgb
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not self.ability_run+1:
			self.game.Sounds.play('shortdrop')
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
			self.game.Sounds.play('dab')
			self.ability_air_side = 1
			self.freeze=2
			self.fire = self.game.effects['flaming_turds'].copy()
			self.ability_run = 1
			self.ability_time = 0.3
	def run_special1(self):
		self.hspeed += (100+(25*((self.maxMoveSpeed-200)/200)))*(self.facing*2-1)
		self.vspeed = 0
		self.gravityMultiplier = 0
		rainbow_poop(self,self.x,self.y-40,not self.facing,yspeed=uniform(-4,4),xspeed=uniform(1,2))
		collisions=[(pygame.Rect(self.hitbox).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack((abs(self.hspeed)/1000)*14*self.attack, self.facing),x[1].damage(5*self.attack))for x in collisions if x[0] and not(x[1] in self.hit_list)]
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
		return self.anim.DAB_ON_HATERS()

	def special2(self):
		self.ability_air_side = 0
		if self.ability_run+1 == 0 and not(self.ability_air):
			self.game.Sounds.play('shortdrop')
			self.ability_air = 1
			self.fire = self.game.effects['flaming_turds'].copy()
			self.ability_run = 2
			self.ability_time = 0.3
	def run_special2(self):
		self.vspeed = -800
		self.gravityMultiplier = 12
		[rainbow_poop(self,self.x,self.y-40,randint(0,1),yspeed=5,xspeed=uniform(0,.25),bounce=1)for x in".."]


	def special3(self):
		if not(self.ability_run+1 or self.ability_delay_time):
			self.game.Sounds.play('tornado')
			self.ability_delay_time = 2
			self.ability_run = 3
			self.ability_time = 2.5
			self.gravityMultiplier = 0.4
			self.image_list = []
			self.level = []
			self.count = 0
			self.image_x = []
			self.surf = pygame.Surface((180,180))
			for x in range(60):
				hue = random()*360
				image = [pygame.transform.scale(x, (60,60)) for x in self.game.effects['flaming_turds'].copy()]
				for i in image:#Randomly change the color of the projectile
					pxarray = pygame.PixelArray(i)
					pxarray.replace((255,  0, 0), tuple([int(255*x) for x in hls_to_rgb(hue, .5,  1)]))
					pxarray.replace((169,  1, 1), tuple([int(255*x) for x in hls_to_rgb(hue, .4, .8)]))
					pxarray.replace((255,112,17), tuple([int(255*x) for x in hls_to_rgb(hue, .6, .7)]))
					pxarray.replace((251,228,30), tuple([int(255*x) for x in hls_to_rgb(hue, .7, .8)]))
					del pxarray
				self.image_list.append(image)
				self.image_x.append((randint(-60,180),randint(0,180),randint(5,20)))
			self.img_len = len(image)
			
	
	def run_special3(self):
		self.count += 1
		self.surf.fill((WHITE))

		for i,j in enumerate(self.image_list): #Blits rainbow projectiles onto surfaces
			self.image_x[i] = (self.image_x[i][0] +self.image_x[i][2],self.image_x[i][1],self.image_x[i][2])
			if self.image_x[i][0] > 180:
				self.image_x[i] = (-60,self.image_x[i][1],self.image_x[i][2])
			self.surf.blit(j[self.count%self.img_len],(self.image_x[i][0],self.image_x[i][1]))
			
		pygame.draw.polygon(self.surf,WHITE,((0,0),(0,180),(60,180)))
		pygame.draw.polygon(self.surf,WHITE,((180,0),(180,180),(120,180)))
		self.surf.set_colorkey((WHITE))
		self.img.append((self.surf,(self.x-90,self.y-180)))
		
		collisions=[(pygame.Rect((self.x-90,self.y-180,180,180)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(12*self.attack, x[1].x>(self.x)),x[1].damage(.5 * self.attack))for x in collisions if x[0] and x[1] != self]
