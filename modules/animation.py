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
		l_hand_offset = pygame.math.Vector2(-28,0).rotate(r_angle/2-90) #generate offsets for hand positions
		r_hand_offset = pygame.math.Vector2(28,0).rotate(l_angle/2+90)
		r_hand, rh_rect = animator.pivot(self.r_hand,l_angle/2+90, r_hand_offset+(128+17,256-81), (7.5,-7.5)) #rotate hands about connecting point
		l_hand, lh_rect = animator.pivot(self.l_hand,r_angle/2-90, l_hand_offset+(128-32+15,256-81), (-7.5,-7.5))
		l_foot_offset = pygame.math.Vector2(0,28).rotate(l_angle) #generate offsets for foot positions
		r_foot_offset = pygame.math.Vector2(0,28).rotate(r_angle)
		r_foot, rf_rect = animator.pivot(self.r_foot,r_angle, r_foot_offset+(128+21,256-45), (-7.5,7.5)) #rotate feet about connecting point
		l_foot, lf_rect = animator.pivot(self.l_foot,l_angle, l_foot_offset+(128-21+15,256-45), (-7.5,7.5))
		bob = 1+abs(r_angle/3) #calculate offset for "bobbing" while walking
		self.surface.blit(r_foot, rf_rect) #blit foot
		self.surface.blit(r_leg, rl_rect) #blit leg
		self.surface.blit(r_hand, rh_rect.move(0,bob)) #blit hand
		self.surface.blit(r_arm, ra_rect.move(0,bob)) #blit arm
		self.surface.blit(self.head, (128-10.5, 256-120 + bob)) #blit body and head
		self.surface.blit(self.body, (128-  21, 256- 99 + bob))
		self.surface.blit(l_foot, lf_rect) #blit foot
		self.surface.blit(l_leg, ll_rect) #blit leg
		self.surface.blit(l_hand, lh_rect.move(0,bob)) #blit hand
		self.surface.blit(l_arm, la_rect.move(0,bob)) #blit arm
		return self.surface

	def DAB_ON_HATERS(self): #i'm sorry.
		if self.anim!="daberoni":self.frame=0;self.anim="daberoni" #reset frame on animation change
		self.surface.fill(0) #clear
		r_arm, ra_rect = animator.pivot(self.r_arm, 190, (128+17,256-81), (15,-7.5))
		l_arm, la_rect = animator.pivot(self.l_arm, 10, (128-32+15,256-81), (-15,-7.5))
		l_hand_offset = pygame.math.Vector2(-28,0).rotate(10) #generate offsets for hand positions
		r_hand_offset = pygame.math.Vector2(28,0).rotate(190)
		r_hand, rh_rect = animator.pivot(self.r_hand, 190, r_hand_offset+(128+17,256-81), (7.5,-7.5)) #rotate hands about connecting point
		l_hand, lh_rect = animator.pivot(self.l_hand,  10, l_hand_offset+(128-32+15,256-81), (-7.5,-7.5))
		rl_rect = (128+ 6,256-45)
		ll_rect = (128-21,256-45)
		l_foot_offset = pygame.math.Vector2(0,28)
		r_foot_offset = pygame.math.Vector2(0,28)
		rf_rect = r_foot_offset+(128+6,256-45)
		lf_rect = l_foot_offset+(128-21,256-45)
		self.surface.blit(self.body, (128-  21, 256- 99))
		self.surface.blit(self.head, (128-10.5, 256-120)) #blit body and head
		self.surface.blit(self.r_foot, rf_rect) #blit foot
		self.surface.blit(self.r_leg, rl_rect) #blit leg
		self.surface.blit(self.l_foot, lf_rect) #blit foot
		self.surface.blit(self.l_leg, ll_rect) #blit leg
		self.surface.blit(l_hand, lh_rect) #blit hand
		self.surface.blit(l_arm, la_rect) #blit arm
		self.surface.blit(r_hand, rh_rect) #blit hand
		self.surface.blit(r_arm, ra_rect) #blit arm
		return self.surface
