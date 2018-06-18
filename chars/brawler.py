import pygame
from settings import *
from math import sin, radians
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not(self.ability_run+1):
			self.dirn = self.facing
			self.charging = self.game.effects['charging'].copy()
			self.ability_run = 0
			self.ability_time = -1
			self.release = 0
			self.freeze = 2
			self.SP0_counter = 60
			self.SP0_go = 0
			self.frame_count = 0
		
	def run_special0(self):#charge punch
		if (self.BTNDown and self.release) or self.SP0_counter > 210:
			self.SP0_go = 1
		else:
			if not(self.SP0_go):
				self.img.append((pygame.transform.scale(self.charging[self.frame_count%98],(40,40)),(self.x-20+(((self.dirn==0)-0.5)*50),self.y-70)))
				self.frame_count += 1
			self.SP0_counter += 1
		if self.SP0_go:
			self.hspeed = (self.dirn-0.5)*2*(self.SP0_counter*10)
			pygame.draw.rect(self.game.win,BLUE,(self.x,self.y-100,(self.dirn-0.5)*2*60,100),3)
			collisions=[(pygame.Rect((self.x+(self.dirn==0)*-60,self.y-100,60,100)).colliderect(x.hitbox),x)for x in self.game.sprites]
			[(x[1].knockBack(self.attack*self.SP0_counter/4, self.dirn),x[1].damage(self.attack *self.SP0_counter /4))for x in collisions if x[0] and not(x[1] in self.hit_list)]
			self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			self.SP0_counter -= 5
			if self.SP0_counter <= 0:
				self.SP0_go = 0
				self.ability_run = 0
				self.ability_time = 0
			return self.anim.punch(self.dirn)
	
	def special1(self, dir):#Side punch
		if not(self.ability_run+1 or self.ability_air):
			self.ability_run = 1
			self.ability_air = 1
			self.ability_time = 0.65
			self.freeze = 2
			self.dir = dir
			self.hspeed = 1800*(dir-0.5)
			self.vspeed = -600
	
	def run_special1(self):
		pygame.draw.rect(self.game.win,BLUE,(self.x-70+((self.dir==1)*(90)), self.y-120, 50, 120),4)
		collisions=[(pygame.Rect((self.x-70+((self.dir==1)*(90)), self.y-120, 50, 120)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(self.attack*20, self.dir),x[1].damage(self.attack *15))for x in collisions if x[0] and not(x[1] in self.hit_list)]
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
		return self.anim.punch(self.dir)
		
	def special2(self):#Jump punch
		if not(self.ability_run+1 or self.ability_air_side):
			self.ability_air_side = 1
			self.freeze = 2
			self.ability_run = 2
			self.ability_time = 0.4
		
	
	def run_special2(self):
		self.vspeed = -500
		pygame.draw.rect(self.game.win,BLUE,(self.x-40, self.y-140, 80, 40),4)
		collisions=[(pygame.Rect((self.x-40, self.y-120, 80, 20)).colliderect(x.hitbox),x)for x in self.game.sprites]
		[(x[1].knockBack(self.attack*20, 2),x[1].damage(self.attack *15))for x in collisions if x[0] and not(x[1] in self.hit_list)]
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
		return self.anim.punch(2)
		
		
	def special3(self):
		if not(self.ability_run+1):
			self.release = 0
			self.ability_run = 3
			self.ability_time = -1
			self.hspeed = 0
			self.freeze = 2
			self.count = 0
			self.hue = 0
			self.open = 0
			self.start = 1
			self.end = 0
			self.hit_list

	def run_special3(self):
		surf = pygame.Surface((1280,720),pygame.SRCALPHA,32)#I was lasy so I made the surface be the entire screen
		if self.start:#Controls the animation
			self.open += 1
			if self.open >= 90:
				self.open = 90
				self.start = False
		elif self.end:
			self.open -= 3
			if self.open <= 0:
				self.open = 0
				self.ability_run = 0
				self.ability_time = 0
			
		self.color = [int(x*255) for x in hls_to_rgb(self.hue/360,0.5,1)]#Controls the color
		self.hue+=1
		if self.hue%30 == 0:
			self.hit_list = []
		#Draws the thing
		pygame.draw.polygon(surf,self.color,((self.x-7,self.y-79),(self.x-10,self.y-72),(self.x-7,self.y-65),(self.x+7,self.y-65),(self.x+10,self.y-72),(self.x+7,self.y-79)))
		pygame.draw.lines(surf,self.color,1,((self.x-(70*sin(radians(self.hue*4))),self.y-72-(70*sin(radians(self.open)))),
													(self.x-(100*sin(radians(self.hue*4))),self.y-72),
													(self.x-(70*sin(radians(self.hue*4))),self.y-72+(70*sin(radians(self.open)))),
													(self.x+(70*sin(radians(self.hue*4))),self.y-72+(70*sin(radians(self.open)))),
													(self.x+(100*sin(radians(self.hue*4))),self.y-72),
													(self.x+(70*sin(radians(self.hue*4))),self.y-72-(70*sin(radians(self.open))))),10)
		self.img.append((surf,(0,0)))
		collisions=[(pygame.Rect((self.x-70,self.y-142,140,142)).colliderect(x.hitbox),x)for x in self.game.objects]
		for x in collisions:
			if x[0] and not(x[1] in self.hit_list):
				x[1].Xspeed *= -1
				x[1].Yspeed *= -1
				x[1].hit_list = [self]
				try: x[1].facing = (x[1].facing==0)
				except: pass
				
		self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
		if self.release:
			self.start = False
			self.end = True
