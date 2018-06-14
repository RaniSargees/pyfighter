import pygame
from math import sin,cos,pi,radians,degrees
from random import randint
from settings import *

class animator():
	def __init__(self,sprite):
		self.surface	= pygame.surface.Surface((256,256))
		self.frame	= 0
		self.anim	= ""

		for x in sprite : x.set_colorkey(GRAEY);x.convert_alpha()
		self.head	= sprite[0]
		self.body	= sprite[1]
		self.l_arm	= sprite[2]
		self.l_arm_1	= sprite[2]
		self.l_arm_2	= sprite[2]
		self.l_hand	= sprite[3]
		self.r_arm	= sprite[4]
		self.r_arm_1	= sprite[4]
		self.r_arm_2	= sprite[4]
		self.r_hand	= sprite[5]
		self.l_leg	= sprite[6]
		self.l_leg_1	= sprite[6]
		self.l_leg_2	= sprite[6]
		self.l_foot	= sprite[7]
		self.r_leg	= sprite[8]
		self.r_leg_1	= sprite[8]
		self.r_leg_2	= sprite[8]
		self.r_foot	= sprite[9]
	def idle(self):
		if self.anim!="idle":self.frame=randint(0,240);self.anim="idle"
		else:self.frame+=1
		self.surface.fill(GRAEY)
		self.surface.blit(self.head, (128-10.5, 256-120+sin(self.frame//30)*2))
		self.surface.blit(self.body, (128-21  , 256-99 +sin(self.frame//30)*2))
		l_arm = pygame.transform.rotozoom(self.l_arm, 90,1)
		r_arm = pygame.transform.rotozoom(self.r_arm,-90,1)
		l_arm.set_colorkey(GRAEY)
		r_arm.set_colorkey(GRAEY)
		l_arm.convert_alpha()
		r_arm.convert_alpha()
		self.surface.blit(l_arm, (128-32, 256-99+sin(self.frame//30)*2))
		self.surface.blit(r_arm, (128+32, 256-99+sin(self.frame//30)*2))
		return self.surface
