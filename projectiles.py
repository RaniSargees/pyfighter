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

class rainbow_poop(pygame.sprite.Sprite):
	def __init__(self, char, x, y, direction, yspeed = -5, xspeed = 2):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.xspeed= xspeed
		self.x = x-24
		self.y = y-24
		self.dir = direction
		self.hit_list = [self,char]
		self.frame = 0
		self.image = [pygame.transform.scale(x, (48,48)) for x in self.char.fire]
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
		if self.y < -500 or self.x > 2080 or self.x < -800 or self.y > 1000:
			print('kill')
			self.kill()

