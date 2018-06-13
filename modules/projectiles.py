from colorsys import hls_to_rgb
from random import random
import pygame
from settings import *

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
			collisions.extend([(pygame.Rect((self.loc[0]+85,self.loc[1]+85,30,30)).colliderect(x.rect),x)for x in self.char.game.ground if not x.platform])
			self.hitTarget = bool(len([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)]))
		if self.go:
			if self.count < self.char.special_1_len*2:
				self.char.game.win.blit(self.explosion[self.count//2],self.loc)
				if self.count < 8:
					pygame.draw.rect(self.char.game.win,BLUE,(self.loc[0]+50,self.loc[1]+50,100,100),4)
					collisions=[(pygame.Rect((self.loc[0]+50,self.loc[1]+50,100,100)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
				else: collisions=[]
				self.count += 1
				[x[1].damage(15*self.char.attack)for x in collisions if x[0]and not(x[1]in self.hit_list)]
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.kill()
		else:
			self.char.game.win.blit(self.explosion[self.count],self.loc)
		if self.loc[0] < -200 or self.loc[0] > 1280:
			self.kill()

class rainbow_poop(pygame.sprite.Sprite):
	def __init__(self, char, x, y, direction, yspeed = -5, xspeed = 2, bounce = 0):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.xspeed= xspeed
		self.x = x-24
		self.y = y-24
		self.bounce = bounce
		self.dir = direction
		self.hit_list = [self,char]
		self.frame = 0
		self.image = [pygame.transform.scale(x, (48,48)) for x in self.char.fire]
		if self.dir-1:self.image=[pygame.transform.flip(x, 1,0) for x in self.image]
		hue = random()*360
		self.yspeed = yspeed
		for x in self.image:
			pxarray = pygame.PixelArray(x)
			pxarray.replace((255,  0, 0), tuple([int(255*x) for x in hls_to_rgb(hue, .5,  1)]))
			pxarray.replace((169,  1, 1), tuple([int(255*x) for x in hls_to_rgb(hue, .4, .8)]))
			pxarray.replace((255,112,17), tuple([int(255*x) for x in hls_to_rgb(hue, .6, .7)]))
			pxarray.replace((251,228,30), tuple([int(255*x) for x in hls_to_rgb(hue, .7, .8)]))
			del pxarray

	def update(self):
		self.char.game.win.blit(self.image[self.frame],(self.x, self.y))
		self.x += (self.dir*2-1) * self.xspeed * 800 * self.char.game.dt
		self.y += self.yspeed
		self.yspeed += 1
		collisions=[(pygame.Rect(x.hitbox).collidepoint(self.x+24, self.y+24), x)for x in self.char.game.sprites]
		collisions=[x[1].damage(1*self.char.attack) for x in collisions[:]if x[1]not in self.hit_list and x[0]]
		if self.y < -500 or self.x > 2080 or self.x < -800 or self.y > 1000 or len(collisions):
			self.kill()
		elif  [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.x+18,self.y+18,12,12)]:
			if not self.bounce:self.kill()
			else:self.bounce-=1;self.yspeed*=-.8;self.xspeed*=.8

class Tinylaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.image = pygame.transform.rotate(pygame.transform.scale(self.char.bullet[0],(20,15)),angle)
		self.image_rect = self.image.get_rect()

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.collision_rect = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.collision_rect), x) for x in self.char.game.sprites]
		collisions=[x[1].damage(1*self.char.attack) for x in collisions[:]if x[1]!=self.char and x[0]]
		if self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000 or len(collisions):
			self.kill()
		elif [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.collision_rect) and x.platform == 0]:
			self.kill()

class laser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x-20,y-15)
		self.image = pygame.transform.rotate(pygame.transform.scale(self.char.bullet[0],(40,30)),angle)
		self.image_rect = self.image.get_rect()

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.collision_rect = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.collision_rect), x) for x in self.char.game.sprites]
		collisions=[x[1].damage(3*self.char.attack) for x in collisions[:]if x[1]!=self.char and x[0]]
		if self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000 or len(collisions):
			self.kill()
		elif [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.collision_rect) and x.platform == 0]:
			self.kill()

class BIGlaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle,facing):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.facing = facing
		self.char = char
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.image = pygame.transform.rotate(self.char.bullet[0],angle)
		self.image_rect = self.image.get_rect()

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.collision_rect = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.collision_rect), x) for x in self.char.game.sprites]
		collisions=[(x[1].knockBack(40*self.char.attack,self.facing),x[1].damage(15*self.char.attack)) for x in collisions[:]if x[1]!=self.char and x[0]]
		if self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000 or len(collisions):
			self.kill()
		elif [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.collision_rect) and x.platform == 0]:
			self.kill()

class Bomblaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0,facing=0):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.facing = facing
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.angle = angle
		self.image = pygame.transform.rotate(self.char.bullet[0],angle)
		self.image_rect = self.image.get_rect()

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.Yspeed += 0.5
		self.collision_rect = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.collision_rect), x) for x in self.char.game.sprites]
		collisions=[(x[1].knockBack(18*self.char.attack,self.facing),x[1].damage(30*self.char.attack)) for x in collisions[:]if x[1]!=self.char and x[0]]
		self.angle += 4
		self.image = pygame.transform.rotate(self.char.bullet[0],self.angle)
		self.image_rect = self.image.get_rect()
		if [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.collision_rect) and x.platform == 0] or len(collisions):
			for i in [[0.707,0.707,-45],[0,1,-90],[-0.707,0.707,-135],[-0.707,-0.707,-180],[-1,0,135],[0,-1,90],[0.707,-0.707,45],[1,0,0]]:
				M_Bomblaser(self.char,self.loc[0],self.loc[1],i[0]*10,(i[1]+1)*-10,angle = i[2],facing=self.facing)
			self.kill()
		elif self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000:
			self.kill()

class M_Bomblaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0,facing=0):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.facing = facing
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.angle = angle
		self.transformed_image = pygame.transform.scale(self.char.bullet[0],(40,30))
		self.image = pygame.transform.rotate(self.transformed_image,angle)
		self.image_rect = self.image.get_rect()

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.Yspeed += 0.5
		self.collision_rect = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.collision_rect), x) for x in self.char.game.sprites]
		collisions=[(x[1].knockBack(4*self.char.attack,self.facing),x[1].damage(5*self.char.attack)) for x in collisions[:]if x[1]!=self.char and x[0]]
		self.angle += 4
		self.image = pygame.transform.rotate(self.transformed_image ,self.angle)
		self.image_rect = self.image.get_rect()
		if [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.collision_rect) and x.platform == 0] or len(collisions):
			for i in [[0.707,0.707,-45],[0,1,-90],[-0.707,0.707,-135],[-0.707,-0.707,-180],[-1,0,135],[0,-1,90],[0.707,-0.707,45],[1,0,0]]:
				Tinylaser(self.char,self.loc[0],self.loc[1],i[0]*40,i[1]*40,i[2])
			self.kill()
		elif self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000:
			self.kill()
