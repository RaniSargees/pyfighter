import pygame
from settings import *
from modules.character import *
from modules.projectiles import *

class char(Char):
	def special0(self):
		if not self.ability_run+1:
			self.game.Sounds.play('pew')
			self.freeze = 2
			self.ability_run = 0
			self.ability_time = 0.01
			self.bullet = self.game.effects['pellet'].copy()
			laser(self,self.x-20,self.y-92-15,((self.facing==1)-0.5)*2*50,0,0)#Shoots laser projectile in the users facing direction

	def run_special0(self):
		pass

	def special1(self,direction):
		if not(self.ability_run+1 or self.ability_delay_time):
			self.game.Sounds.play('extend')
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
		self.ability_delay_time = 1
		if self.whip_phase == 1: #Extend Whip
			self.ability_location = (self.ability_location[0]+25*((self.direction==1)-0.5)*2,self.ability_location[1])
			pygame.draw.line(self.game.win,YELLOW,(self.x,self.y-77),(self.ability_location[0],self.ability_location[1]+15),10)
			self.game.win.blit(self.tip,self.ability_location)
			if abs(self.x - self.ability_location[0]) > 200:#If whip reaches max length goto next phase
				self.whip_phase = 2
				self.currentCord = self.ability_location
			collisions=[(pygame.Rect(x.hitbox).collidepoint(self.ability_location[0]+20, self.ability_location[1]+15), x) for x in self.game.sprites]
			self.target=[x[1] for x in collisions[:]if x[1]!=self and x[0]]
			if self.target != []:#If whip hits a target lock the hit players movement and goto the next phase
				[exec('x.freeze=3') for x in self.target]
				self.whip_phase = 2
				self.currentCord = self.ability_location
		elif self.whip_phase == 2: #Retract whip if it hit a target or reached its max length
			self.diff = ((self.x -self.currentCord[0])/16,((self.y-92)-self.currentCord[1])/16)#calculates the difference between the whips current(When phase 2 started) location and the players (If the player was moving during the whip)
			self.ability_location = (self.ability_location[0]+self.diff[0],self.ability_location[1]+self.diff[1])#Moves it back by a 16th of that distance
			pygame.draw.line(self.game.win,YELLOW,(self.x,self.y-77),(self.ability_location[0],self.ability_location[1]+15),10)
			self.game.win.blit(self.tip,self.ability_location)#Draw the whip
			for char in self.target:
				char.x,char.y = self.ability_location[0],self.ability_location[1]+92
			if abs(self.x - self.ability_location[0]) <= 50:
				if len(self.target):#Stun player grabbed for x amount of seconds dependent on their current dmg and free their movement afterwards
					[exec('x.stun = min((x.dmg/200),0.6);x.freeze = 0') for x in self.target]
					self.whip_phase = 3
					self.timer = 0
					[(char.damage(5*self.attack)) for char in self.target]#deal damage to hooked target
					for char in self.target:
						char.x,char.y = self.x,self.y
						char.gravityMultiplier = 0
				else:
					self.ability_run = 0
					self.ability_time = 0

		elif self.whip_phase == 3:
			self.timer += 1
			if self.timer < 39:#Run phase 3 for 39 frames
				for char in self.target:
					char.gravityMultiplier = 0#Remove gravity while they are being pushed up
					char.x,char.y = char.x+(10*((self.direction==1)-0.5)),char.y-5#Knock up players grabbed
			else:#Reset variables at end
				self.whip_phase = 1
				self.ability_run = 0
				self.ability_time = 0
				self.freeze = 0
				for char in self.target:
					char.gravityMultiplier = 1

			if self.timer%30 == 0:#Shoot a large projectile at knocked up enemy every 30 frames
				self.game.Sounds.play('pew')
				BIGlaser(self,self.x,self.y-92,((self.direction==1)-0.5)*2*20,-20,-45-(90*(self.direction==1)),self.direction)
			elif self.timer%10 == 0:#Shoot a regular projectile at knocked up enemy every 10 frames
				self.game.Sounds.play('pew')
				laser(self,self.x,self.y-92,((self.direction==1)-0.5)*2*25,-25,-45-(90*(self.direction==1)))

	def special2(self):
		if not(self.ability_run+1 or self.ability_air_side):
			self.game.Sounds.play('longpew',maxtime = 1200)
			self.ability_air_side = 1
			self.ability_run = 2
			self.ability_time = 1.2
			self.bullet = self.game.effects['pellet'].copy()
			self.LR = 0
			self.count = 0

	def run_special2(self):
		self.count += 1
		self.vspeed = -200#Launches the player upwards
		self.gravityMultiplier = 0#Removes gravity
		if self.count%3 == 0:#Launches laser projectile downwards from the left or right foot. Changing every 3 frames 
			self.LR+=1
			laser(self,self.x+(((self.LR%2)-0.5)*38)-15,self.y,0,20,90)

	def special3(self):
		if not(self.ability_run+1 or self.ability_delay_time):
			self.game.Sounds.play('pew')
			self.ability_run = 3
			self.ability_time = 0.2
			self.ability_delay_time = 2#Prevents ability being used again for 2 seconds (To prevent spaming)
			self.freeze = 2
			self.bullet = self.game.effects['pellet'].copy()
			Bomblaser(self,self.x,self.y-92,((self.facing==1)-0.5)*20,-10,facing=self.facing)#Launches Bomblaser projectile in its facing direction
	def run_special3(self):
		pass

