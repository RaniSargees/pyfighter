import pygame
from settings import*

class fireball(pygame.sprite.Sprite):
	def __init__(self,char,x,y,direction):
		pygame.sprite.Sprite.__init__(self,char.game.objects)
		self.char = char
		self.loc = (x,y)
		self.dir = direction
		self.hitTarget = 0
		self.count = 0
		self.go = 0
		self.explosion = self.char.explosion
		self.hit_list = [self,char]
	def update(self):
		if self.hitTarget and not(self.count):
			self.go = 1
		elif not(self.count):
			self.loc = (self.loc[0] + (self.dir-0.5)*20,self.loc[1])
			collisions = [(pygame.Rect((self.loc[0]+85,self.loc[1]+85,30,30)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
			self.hitTarget = bool(len([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)]))
		if self.go:
			if self.count < self.char.special_1_len*2:
				self.char.game.win.blit(self.explosion[self.count//2],self.loc)
				if self.count < 8:
					pygame.draw.rect(self.char.game.win,BLUE,(self.loc[0]+50,self.loc[1]+50,100,100),4)
					collisions=[(pygame.Rect((self.loc[0]+50,self.loc[1]+50,100,100)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
				else: collisions=[]
				self.count += 1
				[x[1].damage(15)for x in collisions if x[0]and not(x[1]in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.kill()
		else:
			self.char.game.win.blit(self.explosion[self.count],self.loc)
		if self.loc[0] < -200 or self.loc[0] > 1280:
			self.kill()
