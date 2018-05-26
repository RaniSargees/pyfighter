import pygame
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
	
	def new(self):
		self.canvas = pygame.Surface((640,480),pygame.SRCALPHA,32)
		self.grid = paintCanvis(self.canvas,1,5)
		for i in range(len(COLORS)):
			BTN(self,self.win,i,(30+(i*70)-((i > 8)*630),520+((i > 8)*70),60,60),self.ColorBTN)
		for i in self.ColorBTN:
			if i.cnum == 1:
				i.selected = 1
		
		self.BrushSize = BTN(self,self.win,0,(710,30,50,40),self.MenuBTN,text = str(self.grid.brush),fn = 'self.grid.brush=5;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		BTN(self,self.win,0,(670,30,30,40),self.MenuBTN,text = '<',fn = 'self.grid.brush-=1;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		BTN(self,self.win,0,(770,30,30,40),self.MenuBTN,text = '>',fn = 'self.grid.brush+=1;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		
			
		
	
	def run(self):
		self.playing = 1
		self.Mouse = pygame.mouse.get_pos()
		self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
		while self.playing:
			events = pygame.event.get()
			self.draw()
			self.buttons()
			if self.hold:
				self.Mouse2 = pygame.mouse.get_pos()
				self.Mouse2 = (self.Mouse2[0]-self.shift,self.Mouse2[1]-self.shift)
				self.grid.update(self.Mouse,self.Mouse2)
			else:
				self.grid.update()
			
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.hold = True
				elif event.type == pygame.MOUSEBUTTONUP:
					self.hold = False
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_p:
						self.canvas = pygame.Surface((640,480),pygame.SRCALPHA,32)
						self.grid = paintCanvis(self.canvas,self.grid.color,self.grid.brush)
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

pygame.init()
win = pygame.display.set_mode(RES)
d = paint(win)
d.new()
d.run()
pygame.quit()