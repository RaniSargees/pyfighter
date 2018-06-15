import pygame
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not self.ability_run+1:
			self.dirn = self.facing
			self.ability_run = 0
			sefl.ability_time = -1
			self.release = 0
			self.freeze = 2
			self.SP0_counter = 0
			self.SP0_go = 0
		
	def run_special0(self):
		if (self.BTNDown and self.release) or self.SP0_counter > 180:
			self.SP0_go = 1
		else:
			self.SP0_counter += 1
		if self.SP0_go:
			self.hspeed = (self.facing -0.5)*2*(self.SP0_counter*3)
			self.SP0_counter -= 5
			if self.SP0_counter <= 0:
				self.SP0_go = 0
				self.ability_run = 0
				serlf.ability_time = 0
		
		
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
		self.color = [int(x*255) for x in hls_to_rgb(self.hue/360,0.5,1)]
		self.hue+=1
		pygame.draw.polygon(self.game.win,self.color,((self.x-7,self.y-79),(self.x-10,self.y-72),(self.x-7,self.y-65),(self.x+7,self.y-65),(self.x+10,self.y-72),(self.x+7,self.y-79)))
		if self.release:
			self.ability_run = 0
			self.ability_time = 0
			self.stun = 0.4