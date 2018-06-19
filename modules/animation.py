#		Animation
#Returns character sprites animated

import pygame
from math import sin,cos,asin,acos,radians,degrees
from random import randint
from settings import *
pi=3 # ヽ(｀Д´)ﾉ WHYYYYY

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
		self.l_arm_top	= sprite[2].subsurface((15,0,15,15)) # 15,15
		self.l_arm_bot	= sprite[2].subsurface(( 0,0,15,15)) # 15,15
		self.l_hand 	= sprite[3] # 15,15
		self.r_arm  	= sprite[4] # 30,15
		self.r_arm_top 	= sprite[4].subsurface(( 0,0,15,15)) # 15,15
		self.r_arm_bot 	= sprite[4].subsurface((15,0,15,15)) # 15,15
		self.r_hand 	= sprite[5] # 15,15
		self.l_leg  	= sprite[6] # 15,30
		self.l_leg_top	= sprite[6].subsurface((0, 0,15,15)) # 15,15 #extra body parts (probably wont be used)
		self.l_leg_bot	= sprite[6].subsurface((0,15,15,15)) # 15,15
		self.l_foot 	= sprite[7] # 15,15
		self.r_leg  	= sprite[8] # 15,30
		self.r_leg_top	= sprite[8].subsurface((0, 0,15,15)) # 15,15
		self.r_leg_bot	= sprite[8].subsurface((0,15,15,15)) # 15,15
		self.r_foot 	= sprite[9] # 15,15

	def idle(self, anim=1):
		if self.anim!="idle":self.frame=randint(0,240);self.anim="idle" #reset frame on animation change
		else:self.frame+=anim #update frame
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
		self.surface.blit(l_arm, (128-32, 256-81-7+sin(self.frame/30)*2)) #blit rotated arms and hands (bob up/down)
		self.surface.blit(r_arm, (128+17 , 256-81-7+sin(self.frame/30)*2))
		self.surface.blit(l_hand,(128-32, 256-51-7+sin(self.frame/30)*2))
		self.surface.blit(r_hand,(128+17 , 256-51-7+sin(self.frame/30)*2))
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
		self.surface.blit(r_hand, rh_rect.move(0,bob-9)) #blit hand
		self.surface.blit(r_arm, ra_rect.move(0,bob-9)) #blit arm
		self.surface.blit(self.head, (128-10.5, 256-120 + bob)) #blit body and head
		self.surface.blit(self.body, (128-  21, 256- 99 + bob))
		self.surface.blit(l_foot, lf_rect) #blit foot
		self.surface.blit(l_leg, ll_rect) #blit leg
		self.surface.blit(l_hand, lh_rect.move(0,bob-9)) #blit hand
		self.surface.blit(l_arm, la_rect.move(0,bob-9)) #blit arm
		return self.surface

	def jump(self):
		if self.anim!="jump":self.frame=0;self.anim="jump" #reset frame on animation change
		else: self.frame=min(self.frame+1,20)
		if self.frame < 4: #3 frame animation because I'm not adding actual support for this in character.py
			self.surface.fill(0) #clear
			angle = ((self.frame)%2+1)*7.5


			l_leg_offset = pygame.math.Vector2(0,14).rotate(-angle) #generate offsets for foot positions
			r_leg_offset = pygame.math.Vector2(0,14).rotate(-angle)
			l_foot_offset = l_leg_offset+pygame.math.Vector2(0,14).rotate(angle)
			r_foot_offset = r_leg_offset+pygame.math.Vector2(0,14).rotate(angle)
			r_foot, rf_rect  = animator.pivot(self.r_foot   ,-angle,r_foot_offset+(128+ 6+15,256-45), (-7.5,7.5))
			l_foot, lf_rect  = animator.pivot(self.l_foot   ,-angle,l_foot_offset+(128-21+15,256-45), (-7.5,7.5))
			r_leg1, rl_rect1 = animator.pivot(self.r_leg_top,-angle,              (128+ 6+15,256-45), (-7.5,7.5))
			l_leg1, ll_rect1 = animator.pivot(self.l_leg_top,-angle,              (128-21+15,256-45), (-7.5,7.5))
			r_leg2, rl_rect2 = animator.pivot(self.r_leg_bot,angle, r_leg_offset +(128+ 6+15,256-45), (-7.5,7.5))
			l_leg2, ll_rect2 = animator.pivot(self.l_leg_bot,angle, r_leg_offset +(128-21+15,256-45), (-7.5,7.5))

			self.surface.blit(r_foot, rf_rect) #blit foot
			self.surface.blit(r_leg1, rl_rect1) #blit leg
			self.surface.blit(r_leg2, rl_rect2) #blit leg
			self.surface.blit(self.head, (128-10.5, 256-120)) #blit body and head
			self.surface.blit(self.body, (128-  21, 256- 99))
			self.surface.blit(l_foot, lf_rect) #blit foot
			self.surface.blit(l_leg1, ll_rect1) #blit leg
			self.surface.blit(l_leg2, ll_rect2) #blit leg

			l_arm = pygame.transform.rotate(self.l_arm,  90) #rotate arms and hands (T-Pose to A-pose)
			l_hand= pygame.transform.rotate(self.l_hand, 90)
			r_arm = pygame.transform.rotate(self.r_arm, -90)
			r_hand= pygame.transform.rotate(self.r_hand,-90)
			self.surface.blit(l_arm, (128-32, 256-81-7))
			self.surface.blit(r_arm, (128+17 , 256-81-7))
			self.surface.blit(l_hand,(128-32, 256-51-7))
			self.surface.blit(r_hand,(128+17 , 256-51-7))


		elif self.frame==4: self.surface=self.idle();self.frame=4;self.anim="jump";return self.surface
		return self.surface

	def punch(self, dir):
		if dir not in (2,3):dir=0
		if self.anim!="punch"+str(dir):self.frame=0;self.anim="punch"+str(dir) #reset frame on animation change
		else:self.frame+=1 #update frame
		self.surface.fill(0)

		angle = abs(cos(radians(self.frame*45/2))) * 45 #make the arm bend kinda like \/' hopefully, 8 frames
		static= 45

		tempr = pygame.surface.Surface((256, 256))
		templ = pygame.surface.Surface((256, 256))
		tempr.fill(GRAEY)
		templ.fill(GRAEY)
		tempr.set_colorkey(GRAEY)
		templ.set_colorkey(GRAEY)
		#rotate arms
		r_arm_top, rat_rect = animator.pivot(self.r_arm_top,angle, (128+17,256-81), (7.5,-7.5))
		l_arm_top, lat_rect = animator.pivot(self.l_arm_top,180+static, (128-32+7.5,256-81-15), (-7.5,-7.5))
		rarm_offset = pygame.math.Vector2(14,0).rotate(angle)
		larm_offset = pygame.math.Vector2(14,0).rotate(static)
		r_arm_bot, rab_rect = animator.pivot(self.r_arm_bot, -angle, rarm_offset+(128+17+(15*angle/45),256-81), (7.5,-7.5))
		l_arm_bot, lab_rect = animator.pivot(self.l_arm_bot,180-static, larm_offset+(128-32-7.5,256-81-7.5), (-7.5,-7.5))
		rhand_offset= rarm_offset + pygame.math.Vector2(14,0).rotate(-angle)
		lhand_offset= larm_offset + pygame.math.Vector2(14,0).rotate(-static)
		tempr.blit(self.r_hand, rhand_offset+(128+17,256-81-15))
		templ.blit(self.l_hand, lhand_offset+(128-32-7.5,256-81-15))
		tempr.blit(r_arm_bot, rab_rect) #blit arms
		templ.blit(l_arm_bot, lab_rect)
		tempr.blit(r_arm_top, rat_rect)
		templ.blit(l_arm_top, lat_rect)
		if dir==2: #rotate arms depending on direction
			tempr=pygame.transform.rotate(tempr, 90)
			templ=pygame.transform.rotate(templ, 90)
		elif dir==3:
			tempr=pygame.transform.rotate(tempr, -90)
			templ=pygame.transform.rotate(templ, -90)


		self.surface.blit(self.l_leg, (128-21, 256-45)) #blit non moving objects
		self.surface.blit(self.r_leg, (128+ 6, 256-45))
		self.surface.blit(self.l_foot,(128-21, 256-15))
		self.surface.blit(self.r_foot,(128+ 6, 256-15))
		self.surface.blit(self.head,(128-10.5,256-118))
		self.surface.blit(self.body,(128-21  ,256- 97))

		l_arm = pygame.transform.rotate(self.l_arm,  90)
		l_hand= pygame.transform.rotate(self.l_hand, 90)
		if not dir: #shift arms based on rotation
			self.surface.blit(tempr, (0,0))
			self.surface.blit(templ, (0,0))
		elif dir==2:
			self.surface.blit(tempr, (-24,56))
			self.surface.blit(l_arm, (128-32, 256-81-7))
			self.surface.blit(l_hand,(128-32, 256-51-7))
		elif dir==3:
			self.surface.blit(tempr, (64,24))
			self.surface.blit(l_arm, (128-32, 256-81-7))
			self.surface.blit(l_hand,(128-32, 256-51-7))

		return self.surface


	def DAB_ON_HATERS(self): #i'm sorry.
		if self.anim!="daberoni":self.frame=0;self.anim="daberoni" #reset frame on animation change
		if not self.frame: #only render this once since it's not even animated
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
			self.surface.blit(pygame.transform.rotate(self.head, -15), (128-5, 256-110)) #blit body and head
			self.surface.blit(self.r_foot, rf_rect) #blit foot
			self.surface.blit(self.r_leg, rl_rect) #blit leg
			self.surface.blit(self.l_foot, lf_rect) #blit foot
			self.surface.blit(self.l_leg, ll_rect) #blit leg
			self.surface.blit(l_hand, lh_rect.move(0,-9)) #blit hand
			self.surface.blit(l_arm, la_rect.move(0,-9)) #blit arm
			self.surface.blit(r_hand, rh_rect.move(0,-9)) #blit hand
			self.surface.blit(r_arm, ra_rect.move(0,-9)) #blit arm
			self.frame = 1
		return self.surface
