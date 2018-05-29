import pygame, math
from random import randint
from settings import *
from paintCanvas import *
from BTN import *


class paint():
	def __init__(self,win):
		self.win = win
		self.ColorBTN = pygame.sprite.Group()
		self.MenuBTN = pygame.sprite.Group()
		self.shift = 20
		self.click = False
		self.hold = False
		self.up = True
		self.canvas_new = 0
		self.tool = 1
		self.ani_dir = 0
		self.animate = 0
		#1 = brush
		#2 = circle tool
	
	def new(self):
		self.canvas = pygame.Surface((640,480))
		self.head_rect = (285,80,70,70)
		self.torso_rect = (250,150,140,180)
		self.L_arm_rect = (150,180,100,50)
		self.L_hand_rect = (100,180,50,50)
		self.R_arm_rect = (390,180,100,50)
		self.R_hand_rect = (490,180,50,50)
		self.L_leg_rect = (250,330,50,100)
		self.L_foot_rect = (250,430,50,50)
		self.R_leg_rect = (340,330,50,100)
		self.R_foot_rect = (340,430,50,50)
		self.body_rects_old = [self.head_rect,self.torso_rect,self.L_arm_rect,self.L_hand_rect,self.R_arm_rect,self.R_hand_rect,self.L_leg_rect,self.L_foot_rect,self.R_leg_rect,self.R_foot_rect]
		
		self.head = self.canvas.subsurface(self.head_rect)
		self.head.set_colorkey((192,192,192))
		self.torso = self.canvas.subsurface(self.torso_rect)
		self.torso.set_colorkey((192,192,192))
		self.L_arm = self.canvas.subsurface(self.L_arm_rect)
		self.L_arm.set_colorkey((192,192,192))
		self.L_hand = self.canvas.subsurface(self.L_hand_rect)
		self.L_hand.set_colorkey((192,192,192))
		self.R_arm = self.canvas.subsurface(self.R_arm_rect)
		self.R_arm.set_colorkey((192,192,192))
		self.R_hand = self.canvas.subsurface(self.R_hand_rect)
		self.R_hand.set_colorkey((192,192,192))
		self.L_leg = self.canvas.subsurface(self.L_leg_rect)
		self.L_leg.set_colorkey((192,192,192))
		self.L_foot = self.canvas.subsurface(self.L_foot_rect)
		self.L_foot.set_colorkey((192,192,192))
		self.R_leg = self.canvas.subsurface(self.R_leg_rect)
		self.R_leg.set_colorkey((192,192,192))
		self.R_foot = self.canvas.subsurface(self.R_foot_rect)
		self.R_foot.set_colorkey((192,192,192))
		self.body_surf = [self.head,self.torso,self.L_arm,self.L_hand,self.R_arm,self.R_hand,self.L_leg,self.L_foot,self.R_leg,self.R_foot]
		
		self.body_rects = [(x[0]+self.shift,x[1]+self.shift,x[2],x[3]) for x in self.body_rects_old]
		
		self.grid = paintCanvas(self.canvas,1,5)
		self.canvas_Old = []
		for i in range(len(COLORS)):
			BTN(self,self.win,i,(30+(i*70)-((i > 8)*630),520+((i > 8)*70),60,60),self.ColorBTN)
		for i in self.ColorBTN:
			if i.cnum == 1:
				i.selected = 1
		#Brush Size
		self.BrushSize = BTN(self,self.win,0,(710,30,50,40),self.MenuBTN,text = str(self.grid.brush),fn = 'self.grid.brush=5;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		BTN(self,self.win,0,(670,30,30,40),self.MenuBTN,text = '<',fn = 'self.grid.brush-=1;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		BTN(self,self.win,0,(770,30,30,40),self.MenuBTN,text = '>',fn = 'self.grid.brush+=1;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		#Tools
		BTN(self,self.win,0,(680,80,100,100),self.MenuBTN,text = 'Brush',fn = 'self.tool = 1')
		BTN(self,self.win,0,(680,190,100,100),self.MenuBTN,text = 'Circle', fn = 'self.tool = 2')
	def run(self):
		self.playing = 1
		self.Mouse = pygame.mouse.get_pos()
		self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
		while self.playing:
			events = pygame.event.get()
			self.draw()
			self.buttons()
			if self.hold and self.grid.rect.collidepoint(self.Mouse):
				if not(self.canvas_new): 
					self.canvas_Old.append(self.grid.save)
					self.canvas_new = 1
				self.Mouse2 = pygame.mouse.get_pos()
				self.Mouse2 = (self.Mouse2[0]-self.shift,self.Mouse2[1]-self.shift)
				if self.tool == 1:
					self.grid.update([1,self.Mouse,self.Mouse2])
				elif self.tool == 2:
					self.grid.update([2,self.Mouse])
			else:
				self.grid.update()
			keys = pygame.key.get_pressed()
			if keys[pygame.K_z] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and self.up and self.canvas_Old:
				self.up = False
				pygame.surfarray.blit_array(self.grid.win,self.canvas_Old.pop(-1))
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.hold = True
				elif event.type == pygame.MOUSEBUTTONUP:
					if self.canvas_new:
						self.canvas_new = 0
					self.hold = False
				if event.type == pygame.KEYUP:
					self.up = True
					if event.key == pygame.K_p:
						self.new()
					if event.key == pygame.K_f and self.grid.rect.collidepoint(self.Mouse):
						self.canvas_Old.append(self.grid.save)
						for h,i in enumerate(self.body_rects_old):
							tempRect = pygame.Rect(i)
							if tempRect.collidepoint(self.Mouse):
								self.grid.recursiveFill((self.Mouse[0]-i[0],self.Mouse[1]-i[1]),self.body_surf[h])
								break
						else:
							self.grid.recursiveFill(self.Mouse)

			self.Mouse = pygame.mouse.get_pos()
			self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
			pygame.time.delay(10)
			pygame.display.update()

	def buttons(self):
		for i in self.ColorBTN:
			if i.rect.collidepoint(pygame.mouse.get_pos()):
				if self.hold:
					for j in self.ColorBTN:
						j.update(clicked = 0)
					i.update(clicked = 1)
					self.grid.color = i.cnum
				else:
					i.update(mOver = 1)
			else:
				i.update()

		for i in self.MenuBTN:
			if i.rect.collidepoint(pygame.mouse.get_pos()):
				if self.hold==False and self.click==True:
					self.click = False
					if i.clickable:
						for j in self.MenuBTN:
							j.update(clicked = 0)
						i.update(clicked = 1)
					else:
						i.update(mOver=1)
					exec(i.fn)
				else:
					if self.hold == True:
						self.click = True
					i.update(mOver = 1)
			else:
				i.update()
		if self.grid.brush > 10:
			self.grid.brush = 10
			self.BrushSize.update(newText=str(self.grid.brush))
		elif self.grid.brush < 1:
			self.grid.brush = 1
			self.BrushSize.update(newText=str(self.grid.brush))

	def draw(self):
		self.win.fill(WHITE)
		pygame.draw.line(self.win,BLACK,(17,17),(663,17),6)
		pygame.draw.line(self.win,BLACK,(662,17),(662,502),6)
		pygame.draw.line(self.win,BLACK,(662,502),(17,502),6)
		pygame.draw.line(self.win,BLACK,(17,503),(17,17),6)
		self.win.blit(self.canvas,(self.shift,self.shift))
		pygame.draw.rect(self.win,BLACK,self.body_rects[0],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[1],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[2],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[3],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[3],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[4],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[5],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[6],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[7],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[8],2)
		pygame.draw.rect(self.win,BLACK,self.body_rects[9],2)
		self.ani_dir += 2
		self.animate += math.sin(math.radians(self.ani_dir))*0.1
		self.win.blit(self.head,(890,30+self.animate))
		self.win.blit(self.torso,(855,100+self.animate))
		self.win.blit(pygame.transform.rotate(self.L_arm,90),(805,100+self.animate))
		self.win.blit(pygame.transform.rotate(self.L_hand,90),(805,200+self.animate))
		self.win.blit(pygame.transform.rotate(self.R_arm,-90),(995,100+self.animate))
		self.win.blit(pygame.transform.rotate(self.R_hand,-90),(995,200+self.animate))
		self.win.blit(self.L_leg,(855,280))
		self.win.blit(self.L_foot,(855,380))
		self.win.blit(self.R_leg,(945,280))
		self.win.blit(self.R_foot,(945,380))
		

pygame.init()
win = pygame.display.set_mode(RES)
d = paint(win)
d.new()
d.run()
pygame.quit()