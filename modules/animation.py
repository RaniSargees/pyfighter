import pygame
from math import sin,cos,asin,acos,radians,degrees
from random import randint
from settings import *
pi=3

class animator():

	@staticmethod
	def pivot(surface, angle, centre, offset): #rotate surfaces about a point
		#offset should be a pygame.math.Vector2 (allows for rotating offsets)
		offset = pygame.math.Vector2(offset)
		rotated = pygame.transform.rotate(surface, -angle) #rotate surface
		offset = offset.rotate(angle) #rotate offset
		rect = rotated.get_rect(center=centre+offset) #get offset surface rect
		return rotated,rect #when blitting, use rect as position

	def __init__(self,sprite): #init animator
		self.surface	= pygame.surface.Surface((256,256), pygame.SRCALPHA, 32) #new surface
		self.frame  	= 0
		self.anim   	= ""
		self.head   	= sprite[0] # 21,21 #split sprites into separate variables
		self.body   	= sprite[1] # 42,54
		self.l_arm  	= sprite[2] # 30,15
		self.l_hand 	= sprite[3] # 15,15
		self.r_arm  	= sprite[4] # 30,15
		self.r_hand 	= sprite[5] # 15,15
		self.l_leg  	= sprite[6] # 15,30
		self.l_leg_top	= sprite[6].subsurface(( 0, 0,15,15)) # 15,15 #extra body parts (probably wont be used)
		self.l_leg_bot	= sprite[6].subsurface(( 0,15,15,15)) # 15,15
		self.l_foot 	= sprite[7] # 15,15
		self.r_leg  	= sprite[8] # 15,30
		self.r_leg_top	= sprite[8].subsurface(( 0, 0,15,15)) # 15,15
		self.r_leg_bot	= sprite[8].subsurface(( 0,15,15,15)) # 15,15
		self.r_foot 	= sprite[9] # 15,15

	def idle(self):
		if self.anim!="idle":self.frame=randint(0,240);self.anim="idle" #reset frame on animation change
		else:self.frame+=1 #update frame
		self.surface.fill(0)
		self.surface.blit(self.l_leg, (128-21, 256-45)) #blit non moving objects
		self.surface.blit(self.r_leg, (128+ 6, 256-45))
		self.surface.blit(self.l_foot,(128-21, 256-15))
		self.surface.blit(self.r_foot,(128+ 6, 256-15))
		self.surface.blit(self.head, (128-10.5, 256-118+sin(self.frame/30)*2)) #bob up/down
		self.surface.blit(self.body, (128-21  , 256-97 +sin(self.frame/30)*2))
		l_arm = pygame.transform.rotate(self.l_arm,  90) #rotate arms and hands (T-Pose to A-pose)
		l_hand= pygame.transform.rotate(self.l_hand, 90)
		r_arm = pygame.transform.rotate(self.r_arm, -90)
		r_hand= pygame.transform.rotate(self.r_hand,-90)
		self.surface.blit(l_arm, (128-32, 256-81+sin(self.frame/30)*2)) #blit rotated arms and hands (bob up/down)
		self.surface.blit(r_arm, (128+17 , 256-81+sin(self.frame/30)*2))
		self.surface.blit(l_hand,(128-32, 256-51+sin(self.frame/30)*2))
		self.surface.blit(r_hand,(128+17 , 256-51+sin(self.frame/30)*2))
		return self.surface

	def walk(self,hspeed):
		if self.anim!="walk":self.frame=0;self.anim="walk" #reset frame on animation change
		else: self.frame+=hspeed #update frame by hspeed
		self.surface.fill(0) #clear
		r_angle = sin(self.frame/3000)*15 #generate rotation angle from move speed
		l_angle = -r_angle
		r_leg, rl_rect = animator.pivot(self.r_leg, r_angle, (128+ 6+15,256-45), (-7.5,15)) #rotate arms and legs about connecting point
		l_leg, ll_rect = animator.pivot(self.l_leg, l_angle, (128-21+15,256-45), (-7.5,15))
		r_arm, ra_rect = animator.pivot(self.r_arm, l_angle/2+90, (128+17,256-81), (15,-7.5))
		l_arm, la_rect = animator.pivot(self.l_arm, r_angle/2-90, (128-32+15,256-81), (-15,-7.5))
		self.surface.blit(r_leg, rl_rect) #blit leg
		self.surface.blit(r_arm, ra_rect.move(0,abs(r_angle/3))) #blit arm (bobbing w/ body)
		self.surface.blit(self.head, (128-10.5, 256-120 + abs(r_angle/3))) #blit body and head (bobbing)
		self.surface.blit(self.body, (128-  21, 256- 99 + abs(r_angle/3)))
		self.surface.blit(l_leg, ll_rect) #blit leg
		self.surface.blit(l_arm, la_rect.move(0,abs(r_angle/3))) #blit arm (bobbing w/ body)
		return self.surface
