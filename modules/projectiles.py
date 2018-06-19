#Projectiles
#Contains all projectiles used by characters


from colorsys import hls_to_rgb
from random import random
import pygame
from settings import *

class fireball(pygame.sprite.Sprite):
	def __init__(self,char,x,y,direction):#init variables
		pygame.sprite.Sprite.__init__(self,char.game.objects)
		char.game.Sounds.play('pew')#play sound
		self.char = char
		self.loc = (x,y)#Current location
		self.dir = direction#Player direction
		self.hitTarget = 0
		self.count = 0
		self.go = 0
		self.Xspeed = 20#Speed
		self.Yspeed = 0
		self.explosion = self.char.explosion#Explosion effect
		self.hit_list = [self,char]#Prevent hitting your self
		self.hitbox = (0,0,0,0)
		self.once = 1
	def update(self):
		self.hitbox = (self.loc[0]+50,self.loc[1]+50,100,100)
		if self.hitTarget and not(self.count):
			self.go = 1#Starts rest of object animation and collision
		elif not(self.count):#Moves object in facing direction until it hits a target
			self.loc = (self.loc[0] + (self.dir-0.5)*self.Xspeed,self.loc[1])
			collisions = [(pygame.Rect((self.loc[0]+85,self.loc[1]+85,30,30)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
			collisions.extend([(pygame.Rect((self.loc[0]+85,self.loc[1]+85,30,30)).colliderect(x.rect),x)for x in self.char.game.ground if not x.platform])
			self.hitTarget = bool(len([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)]))
		if self.go:
			if self.once:
				self.once = 0
				self.char.game.Sounds.play('explosion')#Plays explosion sfx
			if self.count < self.char.special_1_len*2:#Plays explosion animation
				self.char.game.win.blit(self.explosion[self.count//2],self.loc)
				if self.count < 8:
					collisions=[(pygame.Rect((self.loc[0]+50,self.loc[1]+50,100,100)).colliderect(x.hitbox),x)for x in self.char.game.sprites]
				else: collisions=[]
				self.count += 1
				[x[1].damage(15*self.char.attack)for x in collisions if x[0]and not(x[1]in self.hit_list)]#Calculates damage and knockback to colliding playerss
				self.hit_list.extend([x[1] for x in collisions if x[0] and not(x[1] in self.hit_list)])
			else:
				self.kill()#Remove object at the end
		else:
			self.char.game.win.blit(self.explosion[self.count],self.loc)
		if self.loc[0] < -200 or self.loc[0] > 1280:
			self.kill()#Remove object if it goes beyond the screen

class rainbow_poop(pygame.sprite.Sprite):
	def __init__(self, char, x, y, direction, yspeed = -5, xspeed = 2, bounce = 0):
		pygame.sprite.Sprite.__init__(self, char.game.objects) #add self to projectile group
		self.char = char #store character
		self.Xspeed= xspeed #set horizontal speed
		self.x = x-24 #store starting coords
		self.y = y-24
		self.bounce = bounce #variable for bounce count
		self.dir = direction #direction to move
		self.hit_list = [self,char] #dont hit the same person twice
		self.image = [pygame.transform.scale(x, (48,48)) for x in self.char.fire] #generate array of sized images
		if self.dir-1:self.image=[pygame.transform.flip(x, 1,0) for x in self.image] #flip images for direction
		self.loop_len = len(self.image) #frame count
		self.frame = 0 #frame
		hue = random()*360 #generate random hue
		self.Yspeed = yspeed #set vertical speed
		for x in self.image: #change colours to random hue
			pxarray = pygame.PixelArray(x)
			pxarray.replace((255,  0, 0), tuple([int(255*x) for x in hls_to_rgb(hue, .5,  1)]))
			pxarray.replace((169,  1, 1), tuple([int(255*x) for x in hls_to_rgb(hue, .4, .8)]))
			pxarray.replace((255,112,17), tuple([int(255*x) for x in hls_to_rgb(hue, .6, .7)]))
			pxarray.replace((251,228,30), tuple([int(255*x) for x in hls_to_rgb(hue, .7, .8)]))
			del pxarray
		self.hitbox =(0,0,0,0)
	def update(self):
		self.hitbox = (self.x+20, self.y+20,8,8) #update hitbox
		self.frame += 1 #increment frame
		self.char.game.win.blit(self.image[self.frame%self.loop_len],(self.x, self.y)) #blit image at position
		self.x += (self.dir*2-1) * self.Xspeed * 800 * self.char.game.dt #move by x speed
		self.y += self.Yspeed #add yspeed
		self.Yspeed += 1 #gravity
		collisions=[(pygame.Rect(x.hitbox).collidepoint(self.x+24, self.y+24), x)for x in self.char.game.sprites] #check for collisions
		collisions=[x[1].damage(1*self.char.attack) for x in collisions[:]if x[1]not in self.hit_list and x[0]] #deal damage
		if self.y < -500 or self.x > 2080 or self.x < -800 or self.y > 1000 or len(collisions): #destroy when offscreen
			self.kill()
		elif  [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.x+18,self.y+18,12,12)]: #bounce off ground
			if not self.bounce:self.kill() #destroy if bounced too many times
			else:self.bounce-=1;self.Yspeed*=-.8;self.Xspeed*=.8

#All laser classes share similar aspects so I wont comment each one.

class laser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0,hit_list=None):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.Xspeed = Xspeed#Sets Xspeed and Yspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)#Starting location
		self.image = pygame.transform.rotate(pygame.transform.scale(self.char.bullet[0],(40,30)),angle)#changes angle of object based on passed angle
		self.image_rect = self.image.get_rect()
		if hit_list == None: self.hit_list = [self.char]#If a specific hit list isn't passed give it it's own character
		else: self.hit_list = [hit_list]
		self.hitbox = (0,0,0,0)#Temporary hit box

	def update(self):
		self.char.game.win.blit(self.image,self.loc)#Blit object onto screen
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)#Move object in given speeds
		self.hitbox = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)#Calculate new hitbox
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.hitbox), x) for x in self.char.game.sprites]#Test for collisions 
		collisions=[x[1].damage(3*self.char.attack) for x in collisions[:]if not(x[1] in self.hit_list) and x[0]]#Deal damage and knock back if they are not in hit_list
		#Kill object if it hits a player or goes off screen
		if self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000 or len(collisions):
			self.kill()
		elif [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox) and x.platform == 0]:
			self.kill()			
			
					
class Tinylaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0,hit_list=None):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.image = pygame.transform.rotate(pygame.transform.scale(self.char.bullet[0],(20,15)),angle)
		self.image_rect = self.image.get_rect()
		if hit_list == None: self.hit_list = self.char
		else: self.hit_list = hit_list
		self.hitbox = (0,0,0,0)

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.hitbox = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.hitbox), x) for x in self.char.game.sprites]
		collisions=[x[1].damage(1*self.char.attack) for x in collisions[:]if not(x[1] in self.hit_list) and x[0]]
		if self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000 or len(collisions):
			self.kill()
		elif [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox) and x.platform == 0]:
			self.kill()

class BIGlaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle,facing,hit_list=None):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.facing = facing
		self.char = char
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.image = pygame.transform.rotate(self.char.bullet[0],angle)
		self.image_rect = self.image.get_rect()
		if hit_list == None: self.hit_list = [self.char]
		else: self.hit_list = [hit_list]
		self.hitbox = (0,0,0,0)

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.hitbox = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.hitbox), x) for x in self.char.game.sprites]
		collisions=[(x[1].knockBack(40*self.char.attack,self.facing),x[1].damage(15*self.char.attack)) for x in collisions[:]if not(x[1] in self.hit_list) and x[0]]
		if self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000 or len(collisions):
			self.kill()
		elif [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox) and x.platform == 0]:
			self.kill()

class Bomblaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0,facing=0,hit_list=None):
		pygame.sprite.Sprite.__init__(self, char.game.objects)
		self.char = char
		self.facing = facing
		self.Xspeed = Xspeed
		self.Yspeed = Yspeed
		self.loc = (x,y)
		self.angle = angle
		self.image = pygame.transform.rotate(self.char.bullet[0],angle)
		self.image_rect = self.image.get_rect()
		if hit_list == None: self.hit_list = [self.char]
		else: self.hit_list = [hit_list]
		self.hitbox = (0,0,0,0)

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.Yspeed += 0.5#Accelerate object downwards
		self.hitbox = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.hitbox), x) for x in self.char.game.sprites]
		collisions=[(x[1].knockBack(18*self.char.attack,self.facing),x[1].damage(30*self.char.attack)) for x in collisions[:]if not(x[1] in self.hit_list) and x[0]]
		self.angle += 4#Constant rotations
		self.image = pygame.transform.rotate(self.char.bullet[0],self.angle)
		self.image_rect = self.image.get_rect()
		if [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox) and x.platform == 0] or len(collisions):
			self.char.game.Sounds.play('pew')
			for i in [[0.707,0.707,-45],[0,1,-90],[-0.707,0.707,-135],[-0.707,-0.707,-180],[-1,0,135],[0,-1,90],[0.707,-0.707,45],[1,0,0]]:
			#Creates 8 new smaller bombs and shoot them in different directions
				M_Bomblaser(self.char,self.loc[0],self.loc[1],i[0]*10,(i[1]+1)*-10,angle = i[2],facing=self.facing,hit_list = self.hit_list)
			self.kill()
		elif self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000:
			self.kill()

class M_Bomblaser(pygame.sprite.Sprite):
	def __init__(self,char,x,y,Xspeed,Yspeed,angle=0,facing=0,hit_list=None):
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
		if hit_list == None: self.hit_list = [self.char]
		else: self.hit_list = [hit_list]
		self.hitbox = (0,0,0,0)

	def update(self):
		self.char.game.win.blit(self.image,self.loc)
		self.loc = (self.loc[0]+self.Xspeed,self.loc[1]+self.Yspeed)
		self.Yspeed += 0.5#Accelerate object downwards
		self.hitbox = (self.loc[0]+self.image_rect[2]//4,self.loc[1]+self.image_rect[3]//4,self.image_rect[2]//2,self.image_rect[3]//2)
		collisions=[(pygame.Rect(x.hitbox).colliderect(self.hitbox), x) for x in self.char.game.sprites]
		collisions=[(x[1].knockBack(4*self.char.attack,self.facing),x[1].damage(5*self.char.attack)) for x in collisions[:]if not(x[1] in self.hit_list) and x[0]]
		self.angle += 4
		self.image = pygame.transform.rotate(self.transformed_image ,self.angle)
		self.image_rect = self.image.get_rect()
		if [x for x in self.char.game.ground if pygame.Rect(x.rect).colliderect(self.hitbox) and x.platform == 0] or len(collisions):
			for i in [[0.707,0.707,-45],[0,1,-90],[-0.707,0.707,-135],[-0.707,-0.707,-180],[-1,0,135],[0,-1,90],[0.707,-0.707,45],[1,0,0]]:
			#Creates 8 new tiny lasers that goes in 8 different directions
				Tinylaser(self.char,self.loc[0],self.loc[1],i[0]*40,i[1]*40,i[2],hit_list = self.hit_list)
			self.kill()
		elif self.loc[1] < -500 or self.loc[0] > 2080 or self.loc[0] < -800 or self.loc[1] > 1000:
			self.kill()
