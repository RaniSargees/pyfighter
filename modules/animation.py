import pygame
from math import sin,cos,pi,radians,degrees
from settings import *

class animator():
	def __init__(self,sprite):
		self.surface	= pygame.surface.Surface((256,256))
		self.frame	= 0
		self.anim	= "idle"
		self.head	= sprite[0]
		self.body	= sprite[1]
		self.l_arm_1	= sprite[2]
		self.l_arm_2	= sprite[2]
		self.l_hand	= sprite[3]
		self.r_arm_1	= sprite[4]
		self.r_arm_2	= sprite[4]
		self.r_hand	= sprite[5]
		self.l_leg_1	= sprite[6]
		self.l_leg_2	= sprite[6]
		self.l_foot	= sprite[7]
		self.r_leg_1	= sprite[8]
		self.r_leg_2	= sprite[8]
		self.r_foot	= sprite[9]
	def idle(self):
		if self.anim!="idle":self.frame=0;self.anim="idle"
		else:self.frame+=1
		self.surface.fill(GRAEY)
		self.surface.blit(self.head, (128-10.5, 256-120+sin(frame)*2))
		self.surface.blit(self.body, (128-21, 256-99+sin(frame)*2))
