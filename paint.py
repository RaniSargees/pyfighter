import pygame, math, os
from random import randint
from settings import *
from paintCanvas import *
from BTN import *
from text_box import *


class paint():
	def __init__(self,win,directory=None,img_lst = []):
		self.win = win
		self.ColorBTN = pygame.sprite.Group()
		self.MenuBTN = pygame.sprite.Group()
		self.Misc = pygame.sprite.Group()
		self.Classes = pygame.sprite.Group()
		self.shift = 20
		self.click = False
		self.hold = False
		self.up = True
		self.icons = img_lst
		self.canvas_new = 0
		self.undo = 0
		self.save = 0
		self.running = 1
		self.boxUpdate = 0
		self.directory = directory
		self.ani_dir = 0
		self.animate = 0
		self.popUp = 0
		self.popUp_durration = 0
		self.good = 0
		self.tool = 1
		#1 = brush
		#2 = circle tool
		self.Class = 0
		#Boom boi, Sword kid, Pew Pew Kiddi, That one kid who likes to punch stuff, that one guy who shat out skittles durring class
		#    0			1			2							3										4
		self.attack = 1
		self.defense = 1
		self.speed = 1
		#[atk,def,speed]
		
		#Fonts
		self.font = pygame.font.SysFont('Courier New',48)
		self.font_M = pygame.font.SysFont('Courier New',36)
		self.font_S = pygame.font.SysFont('Courier New',24)
		self.font_SS = pygame.font.SysFont('Courier New',16)

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
			if i == 17 and self.icons != []:
				BTN(self.win,i,(30+(i*70)-((i > 8)*630),520+((i > 8)*70),60,60),self.ColorBTN,image = pygame.transform.scale(self.icons['eraser'].copy(),(60,60)))
			else:
				BTN(self.win,i,(30+(i*70)-((i > 8)*630),520+((i > 8)*70),60,60),self.ColorBTN)
		for i in self.ColorBTN:
			if i.cnum == 1:
				i.selected = 1
		#Brush Size
		self.BrushSize = BTN(self.win,0,(710,60,50,40),self.MenuBTN,text = str(self.grid.brush),fn = 'self.grid.brush=5;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		BTN(self.win,0,(670,60,30,40),self.MenuBTN,text = '<',fn = 'self.grid.brush-=1;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		BTN(self.win,0,(770,60,30,40),self.MenuBTN,text = '>',fn = 'self.grid.brush+=1;self.BrushSize.update(newText=str(self.grid.brush))',clickable = False)
		#Tools
		BTN(self.win,0,(685,110,100,100),self.MenuBTN,text = 'Brush',fn = 'self.tool = 1')
		BTN(self.win,0,(685,220,100,100),self.MenuBTN,text = 'Circle', fn = 'self.tool = 2')
		BTN(self.win,0,(685,330,100,100),self.MenuBTN,text = 'Fill', fn = 'self.tool = 3')
		BTN(self.win,0,(685,440,100,100),self.MenuBTN,text = 'Undo', fn = 'self.undo = 1',clickable = False)
		BTN(self.win,0,(685,550,100,100),self.MenuBTN,text = 'Save', fn = 'self.save = 1',clickable = False)
		BTN(self.win,0,(1000,10,250,50),self.MenuBTN,text = 'Return to Main Menu', fn = 'self.playing = 0')
		#Text box
		self.box = Text_Box(self.win,(670,20,130,30),title = 'Character Name')
		#Stats
		BTN(self.win,12,(850,555,30,30),self.MenuBTN,text= '-',clickColor = (0,0,0), circle =1,clickable = False,fn='self.attack-=1')
		BTN(self.win,12,(1165,555,30,30),self.MenuBTN,text= '+',clickColor = (0,0,0), circle =1,clickable = False,fn='self.attack+=(1*(self.attack+self.defense+self.speed < 18))')
		BTN(self.win,12,(850,605,30,30),self.MenuBTN,text= '-',clickColor = (0,0,0), circle =1,clickable = False,fn='self.defense-=1')
		BTN(self.win,12,(1165,605,30,30),self.MenuBTN,text= '+',clickColor = (0,0,0), circle =1,clickable = False,fn='self.defense+=(1*(self.attack+self.defense+self.speed < 18))')
		BTN(self.win,12,(850,655,30,30),self.MenuBTN,text= '-',clickColor = (0,0,0), circle =1,clickable = False,fn='self.speed-=1')
		BTN(self.win,12,(1165,655,30,30),self.MenuBTN,text= '+',clickColor = (0,0,0), circle =1,clickable = False,fn='self.speed+=(1*(self.attack+self.defense+self.speed < 18))')
		#Classes
		BTN(self.win,0,(1050,200,90,90),self.Classes,text='Mage',fn='self.Class = 0')
		BTN(self.win,0,(1150,200,90,90),self.Classes,text='друг',fn='self.Class = 1')
		BTN(self.win,0,(1050,300,90,90),self.Classes,text='Sword',fn='self.Class = 2')
		BTN(self.win,0,(1150,300,90,90),self.Classes,text='Guns',fn='self.Class = 3')
		
		
		self.surf = pygame.Surface((280,150),pygame.SRCALPHA,32)
		pygame.draw.rect(self.surf,GRAEY,(25,5,250,30))
		pygame.draw.rect(self.surf,BLACK,(25,5,250,30),1)
		pygame.draw.rect(self.surf,GRAEY,(25,55,250,30))
		pygame.draw.rect(self.surf,BLACK,(25,55,250,30),1)
		pygame.draw.rect(self.surf,GRAEY,(25,105,250,30))
		pygame.draw.rect(self.surf,BLACK,(25,105,250,30),1)
		pygame.draw.circle(self.surf,GRAY,(25,20),20)
		pygame.draw.circle(self.surf,BLACK,(25,20),20,1)
		pygame.draw.circle(self.surf,GRAY,(25,70),20)
		pygame.draw.circle(self.surf,BLACK,(25,70),20,1)
		pygame.draw.circle(self.surf,GRAY,(25,120),20)
		pygame.draw.circle(self.surf,BLACK,(25,120),20,1)
		try:
			self.surf.blit(pygame.transform.scale(self.icons['attack'].copy(),(20,20)),(15,10))
			self.surf.blit(pygame.transform.scale(self.icons['defense'].copy(),(20,20)),(15,60))
			self.surf.blit(pygame.transform.scale(self.icons['speed'].copy(),(20,20)),(15,110))
		except: pass
		
	def run(self):
		self.playing = 1
		self.Mouse = pygame.mouse.get_pos()
		self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
		while self.playing:
			events = pygame.event.get()
			self.win.fill(WHITE)
			self.buttons()
			self.draw()
			if self.boxUpdate:
				self.box.update(1,events)
			else:
				self.box.update(0)
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
				elif self.tool == 3:
					for h,i in enumerate(self.body_rects_old):
						tempRect = pygame.Rect(i)
						if tempRect.collidepoint(self.Mouse):
							self.grid.flood_fill((self.Mouse[0]-i[0],self.Mouse[1]-i[1]),self.body_surf[h])
							break
			else:
				self.grid.update()
			keys = pygame.key.get_pressed()
			if ((keys[pygame.K_z] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and self.up) or self.undo == 1) and self.canvas_Old:
				self.up = False
				self.undo = 0
				self.grid.win.blit(self.canvas_Old.pop(-1),(0,0))
			if (keys[pygame.K_s] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and self.up) or self.save == 1:
				self.save = 0
				self.popUp = 1
				self.popUp_durration = 0
				try:
					if self.box.text == '':
						0/0
					self.Savedirectory = (self.directory+'\\'+str(self.box.text))
					if not os.path.exists(self.Savedirectory):
						os.makedirs(self.Savedirectory)
					pygame.image.save(self.canvas,self.Savedirectory+'\\'+"Char.png")
					f = open(self.Savedirectory+'\\'+'data.txt',"w+")
					f.write(str([self.Class,[self.attack,self.defense,self.speed]]))
					f.close()
					os.rename(self.Savedirectory+'\\'+'data.txt',self.Savedirectory+'\\'+"!data.trash")
					self.good = 1
				except:
					self.good = 0
				
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
					self.running = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.box.rect.collidepoint(pygame.mouse.get_pos()):
						self.boxUpdate = 1
					else:
						self.boxUpdate = 0
					self.hold = True
				elif event.type == pygame.MOUSEBUTTONUP:
					if self.canvas_new:
						self.canvas_new = 0
					self.hold = False
				if event.type == pygame.KEYUP:
					self.up = True
#					if event.key == pygame.K_p:
#						self.new()
					if event.key == pygame.K_RETURN:
						self.boxUpdate = 0
#					if event.key == pygame.K_f and self.grid.rect.collidepoint(self.Mouse):
#						self.canvas_Old.append(self.grid.save)
#						for h,i in enumerate(self.body_rects_old):
#							tempRect = pygame.Rect(i)
#							if tempRect.collidepoint(self.Mouse):
#								self.grid.flood_fill((self.Mouse[0]-i[0],self.Mouse[1]-i[1]),self.body_surf[h])
#								break
#						else:
#							self.grid.recursiveFill(self.Mouse)

			self.Mouse = pygame.mouse.get_pos()
			self.Mouse = (self.Mouse[0]-self.shift,self.Mouse[1]-self.shift)
			pygame.time.delay(10)
			pygame.display.update()

	def buttons(self):
		#Button updates
		for i in self.Classes:
			if i.rect.collidepoint(pygame.mouse.get_pos()):
				if self.hold==False and self.click==True:
					self.click = False
					if i.clickable:
						for j in self.Classes:
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
		if self.grid.brush > 20:
			self.grid.brush = 20
			self.BrushSize.update(newText=str(self.grid.brush))
		elif self.grid.brush < 1:
			self.grid.brush = 1
			self.BrushSize.update(newText=str(self.grid.brush))

	def draw(self):
		#Canvas
		pygame.draw.line(self.win,BLACK,(17,17),(663,17),6)
		pygame.draw.line(self.win,BLACK,(662,17),(662,502),6)
		pygame.draw.line(self.win,BLACK,(662,502),(17,502),6)
		pygame.draw.line(self.win,BLACK,(17,503),(17,17),6)
		self.win.blit(self.canvas,(self.shift,self.shift))
		#Body parts
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
		self.ani_dir += 2 #Animation delay
		self.animate += math.sin(math.radians(self.ani_dir))*0.1
		self.win.blit(self.head,(890,30+self.animate+1))
		self.win.blit(self.torso,(855,100+self.animate+1))
		self.win.blit(pygame.transform.rotate(self.L_arm,90),(825,130+self.animate+1))
		self.win.blit(pygame.transform.rotate(self.L_hand,90),(825,230+self.animate+1))
		self.win.blit(pygame.transform.rotate(self.R_arm,-90),(975,130+self.animate+1))
		self.win.blit(pygame.transform.rotate(self.R_hand,-90),(975,230+self.animate+1))
		self.win.blit(self.L_leg,(855,280))
		self.win.blit(self.L_foot,(855,380))
		self.win.blit(self.R_leg,(945,280))
		self.win.blit(self.R_foot,(945,380))
		
		#Stat select
		self.win.blit(self.surf,(880,550))
		self.attack = min(max(1,self.attack),11)
		self.defense = min(max(1,self.defense),11)
		self.speed = min(max(1,self.speed),11)
		#Texts
		text = self.font_S.render('Points Remaining:'+str(18-(self.attack+self.defense+self.speed)),True,BLACK)
		text2 = self.font_S.render('Select a Class',True,BLACK)
		text3 = self.font_M.render('Choose your Stats',True,BLACK)
		self.win.blit(text,text.get_rect(center=(1020,530)))
		self.win.blit(text2,text2.get_rect(center=(1145,180)))
		self.win.blit(text3,text3.get_rect(center=(1020,490)))
		pygame.draw.line(self.win,BLACK,(1050,188),(1240,188),1)
		pygame.draw.line(self.win,BLACK,(1050,190),(1240,190),1)
		#Stat box
		for i in range(self.attack):
			pygame.draw.rect(self.win,GREEN,(930+(i*20),557,20,26))
			
		for j in range(self.defense):
			pygame.draw.rect(self.win,GREEN,(930+(j*20),607,20,26))
			
		for k in range(self.speed):
			pygame.draw.rect(self.win,GREEN,(930+(k*20),657,20,26))
		
		for l in range(11):
			pygame.draw.rect(self.win,(0,0,0),(930+(l*20),557,20,26),2)
			pygame.draw.rect(self.win,(0,0,0),(930+(l*20),607,20,26),2)
			pygame.draw.rect(self.win,(0,0,0),(930+(l*20),657,20,26),2)
		
		#Popup when saving
		if self.popUp:
			if not(self.popUp_durration):
				self.popUp_alpha = 255
				self.popUp_surf = pygame.Surface((1280,60))
				if self.good:
					self.popUp_surf.fill((0,255,0))
					self.text = self.font.render('Character has been sucessfully created',True,WHITE)
				else:
					self.popUp_surf.fill((255,0,0))
					self.text = self.font.render('Error: Please fill in Character Name',True,WHITE)
				self.text_rect = self.text.get_rect(center=(640,30))
				self.popUp_surf.blit(self.text,self.text_rect)
				self.popUp_durration = 3
				self.time = pygame.time.Clock()
			self.time.tick()
			self.popUp_alpha -= (self.time.get_time()/1000)*(255/self.popUp_durration)
			self.popUp_surf.set_alpha(self.popUp_alpha)
			if self.popUp_alpha > 0:
				self.win.blit(self.popUp_surf,(0,330))
			else:
				self.popUp = 0
				self.popUp_durration = 0
				

if __name__ == "__main__":
	pygame.init()
	win = pygame.display.set_mode(RES)
	d = paint(win)
	d.new()
	d.run()
	pygame.quit()
