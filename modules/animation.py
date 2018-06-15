import pygame
from math import sin,cos,asin,acos,radians,degrees
from random import randint
from settings import *
pi=3

class animator():

	@staticmethod
	def pivot(surface, angle, centre, offset):
		#offset should be a pygame.math.Vector2
		offset = pygame.math.Vector2(offset)
		rotated = pygame.transform.rotate(surface, -angle)
		offset = offset.rotate(angle)
		rect = rotated.get_rect(center=centre+offset)
		return rotated,rect

	def __init__(self,sprite):
		self.surface	= pygame.surface.Surface((256,256), pygame.SRCALPHA, 32)
		self.frame  	= 0
		self.anim   	= ""
		self.head   	= sprite[0] # 21,21
		self.body   	= sprite[1] # 42,54
		self.l_arm  	= sprite[2] # 30,15
		self.l_hand 	= sprite[3] # 15,15
		self.r_arm  	= sprite[4] # 30,15
		self.r_hand 	= sprite[5] # 15,15
		self.l_leg  	= sprite[6] # 15,30
		self.l_leg_top	= sprite[6].subsurface(( 0, 0,15,15)) # 15,15
		self.l_leg_bot	= sprite[6].subsurface(( 0,15,15,15)) # 15,15
		self.l_foot 	= sprite[7] # 15,15
		self.r_leg  	= sprite[8] # 15,30
		self.r_leg_top	= sprite[8].subsurface(( 0, 0,15,15)) # 15,15
		self.r_leg_bot	= sprite[8].subsurface(( 0,15,15,15)) # 15,15
		self.r_foot 	= sprite[9] # 15,15

	def idle(self):
		if self.anim!="idle":self.frame=randint(0,240);self.anim="idle"
		else:self.frame+=1
		self.surface.fill(0)
		self.surface.blit(self.l_leg, (128-21, 256-45))
		self.surface.blit(self.r_leg, (128+ 6, 256-45))
		self.surface.blit(self.l_foot,(128-21, 256-15))
		self.surface.blit(self.r_foot,(128+ 6, 256-15))
		self.surface.blit(self.head, (128-10.5, 256-118+sin(self.frame/30)*2))
		self.surface.blit(self.body, (128-21  , 256-97 +sin(self.frame/30)*2))
		l_arm = self.l_arm .copy()
		r_arm = self.r_arm .copy()
		l_hand= self.l_hand.copy()
		r_hand= self.r_hand.copy()
		l_arm = pygame.transform.rotate(l_arm,  90)
		l_hand= pygame.transform.rotate(l_hand, 90)
		r_arm = pygame.transform.rotate(r_arm, -90)
		r_hand= pygame.transform.rotate(r_hand,-90)
		self.surface.blit(l_arm, (128-32, 256-81+sin(self.frame/30)*2))
		self.surface.blit(r_arm, (128+17 , 256-81+sin(self.frame/30)*2))
		self.surface.blit(l_hand,(128-32, 256-51+sin(self.frame/30)*2))
		self.surface.blit(r_hand,(128+17 , 256-51+sin(self.frame/30)*2))
		return self.surface

	def walk(self,hspeed):
		if self.anim!="walk":self.frame=0;self.anim="walk"
		else: self.frame+=hspeed
		self.surface.fill(0)
		r_angle = sin(self.frame/3000)*15
		l_angle = -r_angle
		r_leg, r_rect = animator.pivot(self.r_leg, r_angle, (128+6+15,256-45+7.5), (-7.5,15))
		l_leg, l_rect = animator.pivot(self.l_leg, l_angle, (128-21+15,256-45+7.5), (-7.5,15))
		self.surface.blit(r_leg, r_rect)
		self.surface.blit(self.head, (128-10.5, 256-120))
		self.surface.blit(self.body, (128-21  , 256- 99))
		self.surface.blit(l_leg, l_rect)
		return self.surface
		#TODO everything

