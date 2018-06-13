import pygame
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not self.ability_run+1:
			self.freeze = 2
			self.ability_run = 0
			self.ability_time = 0.01
			self.bullet = self.game.effects['pellet'].copy()
			laser(self,self.x,self.y-92,((self.facing==1)-0.5)*2*50,0,0)

	def run_special0(self):
		pass

	def special1(self,direction):
		if not self.ability_run+1:
			self.freeze = 2
			self.direction = direction
			self.ability_run = 1
			self.ability_time = -1
			self.whip_phase = 1
			self.bullet = self.game.effects['pellet'].copy()
			self.target = []
			self.tip = pygame.transform.scale(self.game.effects['pellet'][0].copy(),(40,30))
			self.ability_location = (self.x,self.y-92)

	def run_special1(self):
		if self.whip_phase == 1: #Extend Whip
			self.ability_location = (self.ability_location[0]+25*((self.direction==1)-0.5)*2,self.ability_location[1])
			pygame.draw.line(self.game.win,YELLOW,(self.x,self.y-77),(self.ability_location[0],self.ability_location[1]+15),10)
			self.game.win.blit(self.tip,self.ability_location)
			if abs(self.x - self.ability_location[0]) > 400:
				self.whip_phase = 2
				self.currentCord = self.ability_location
			collisions=[(pygame.Rect(x.hitbox).collidepoint(self.ability_location[0]+20, self.ability_location[1]+15), x) for x in self.game.sprites]
			self.target=[x[1] for x in collisions[:]if x[1]!=self and x[0]]
			if self.target != []:
				[exec('x.freeze=3') for x in self.target]
				self.whip_phase = 2
				self.currentCord = self.ability_location
		elif self.whip_phase == 2: #Retract whip if it hit a target or reached its max length
			self.diff = ((self.x -self.currentCord[0])/16,((self.y-92)-self.currentCord[1])/16)
			self.ability_location = (self.ability_location[0]+self.diff[0],self.ability_location[1]+self.diff[1])
			pygame.draw.line(self.game.win,YELLOW,(self.x,self.y-77),(self.ability_location[0],self.ability_location[1]+15),10)
			self.game.win.blit(self.tip,self.ability_location)
			for char in self.target:
				char.x,char.y = self.ability_location[0],self.ability_location[1]+92
			if abs(self.x - self.ability_location[0]) <= 50:
				if len(self.target):
					[exec('x.stun = min((x.dmg/200),0.6);x.freeze = 0') for x in self.target]
					self.whip_phase = 3
					self.timer = 0
					[(char.damage(5*self.attack)) for char in self.target]
					for char in self.target:
						char.x,char.y = self.x,self.y
						char.gravityMultiplier = 0
				else:
					self.ability_run = 0
					self.ability_time = 0

		elif self.whip_phase == 3:
			self.timer += 1
			if self.timer < 39:
				for char in self.target:
					char.gravityMultiplier = 0
					char.x,char.y = char.x+(10*((self.direction==1)-0.5)),char.y-5
			else:
				self.whip_phase = 1
				self.ability_run = 0
				self.ability_time = 0
				self.freeze = 0
				for char in self.target:
					char.gravityMultiplier = 1

			if self.timer%30 == 0:
				BIGlaser(self,self.x,self.y-92,((self.direction==1)-0.5)*2*20,-20,-45-(90*(self.direction==1)),self.direction)
			elif self.timer%10 == 0:
				laser(self,self.x,self.y-92,((self.direction==1)-0.5)*2*25,-25,-45-(90*(self.direction==1)))

	def special2(self):
		if not(self.ability_run+1 or self.ability_air_side):
			self.ability_air_side = 1
			self.ability_run = 2
			self.ability_time = 1.2
			self.bullet = self.game.effects['pellet'].copy()
			self.LR = 0
			self.count = 0

	def run_special2(self):
		self.count += 1
		self.vspeed = -200
		self.gravityMultiplier = 0
		if self.count%3 == 0:
			self.LR+=1
			laser(self,self.x+(((self.LR%2)-0.5)*48)-15,self.y,0,20,90)

	def special3(self):
		if not(self.ability_run+1 or self.ability_delay_time):
			self.ability_run = 3
			self.ability_time = 0.2
			self.ability_delay_time = 2
			self.freeze = 2
			self.bullet = self.game.effects['pellet'].copy()
			Bomblaser(self,self.x,self.y-92,((self.facing==1)-0.5)*20,-10,facing=self.facing)

	def run_special3(self):
		pass

