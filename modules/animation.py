import pygame
from math import sin,cos,pi,radians,degrees
from random import randint
from settings import *

class animator():
	def __init__(self,sprite):
		self.surface	= pygame.surface.Surface((256,256), pygame.SRCALPHA, 32)
		self.frame  	= 0
		self.anim   	= ""
		self.head   	= sprite[0]
		self.body   	= sprite[1]
		self.l_arm  	= sprite[2]
		self.l_arm_1	= sprite[2]
		self.l_arm_2	= sprite[2]
		self.l_hand 	= sprite[3]
		self.r_arm  	= sprite[4]
		self.r_arm_1	= sprite[4]
		self.r_arm_2	= sprite[4]
		self.r_hand 	= sprite[5]
		self.l_leg  	= sprite[6]
		self.l_leg_1	= sprite[6]
		self.l_leg_2	= sprite[6]
		self.l_foot 	= sprite[7]
		self.r_leg  	= sprite[8]
		self.r_leg_1	= sprite[8]
		self.r_leg_2	= sprite[8]
		self.r_foot 	= sprite[9]

	def idle(self):
		if self.anim!="idle":self.frame=randint(0,240);self.anim="idle"
		else:self.frame+=1
		self.surface.fill(0)
		self.surface.blit(self.l_leg, (128-21, 256-45))
		self.surface.blit(self.r_leg, (128+ 6, 256-45))
		self.surface.blit(self.l_foot,(128-21, 256-15))
		self.surface.blit(self.r_foot,(128+ 6, 256-15))
		self.surface.blit(self.head, (128-10.5, 256-118+sin(self.frame//30)*2))
		self.surface.blit(self.body, (128-21  , 256-97 +sin(self.frame//30)*2))
		l_arm = self.l_arm .copy()
		r_arm = self.r_arm .copy()
		l_hand= self.l_hand.copy()
		r_hand= self.r_hand.copy()
		l_arm = pygame.transform.rotate(l_arm,  90)
		l_hand= pygame.transform.rotate(l_hand, 90)
		r_arm = pygame.transform.rotate(r_arm, -90)
		r_hand= pygame.transform.rotate(r_hand,-90)
		l_arm.set_colorkey(GRAEY) #colorkey has to be set twice because pygame sucks
		r_arm.set_colorkey(GRAEY)
		l_hand.set_colorkey(GRAEY)
		r_hand.set_colorkey(GRAEY)
		self.surface.blit(l_arm, (128-32, 256-81+sin(self.frame//30)*2))
		self.surface.blit(r_arm, (128+17 , 256-81+sin(self.frame//30)*2))
		self.surface.blit(l_hand,(128-32, 256-51+sin(self.frame//30)*2))
		self.surface.blit(r_hand,(128+17 , 256-51+sin(self.frame//30)*2))
		return self.surface
