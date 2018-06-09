import pygame, os, zipfile
from paint import *
from game import *
from settings import *
from joystick_wrapper import *
from map import *
from BTN import *

class GUI():
	def __init__(self,win,joysticks):
		self.win = win
		self.joysticks = joysticks
		self.bg = None
		self.img = []
		self.mDown = 0
		self.pos = (0,0)
		self.BTN_list = []
		#Location Index:
		#	0, Main Menu
		#	1, Character Select
		#	2, Map Select
		#	3, Options

	def new(self,location=0):
		self.load_data()
		self.MenuBTN = pygame.sprite.Group()
		self.img = []
		self.img.append([self.bg,(0,0)]) #Background image
		if location == 0: #Main Menu
			#Title Text
			self.font = pygame.font.SysFont('Comic Sans MS',144)
			self.text = self.font.render('PYFIGHTER',True,BLACK)
			self.text_rect = self.text.get_rect(center=(640,180))
			self.img.append([self.text,self.text_rect])
			#Buttons
			self.BTN_list = [[BTN(self.win,0,(140,300,600,200),self.MenuBTN,text='PLAY',fn='self.new(1)',thickness = 2),
							BTN(self.win,0,(840,300,300,200),self.MenuBTN,text='CREATE',fn='self.run_paint()',thickness = 2)],
							[BTN(self.win,0,(140,550,600,100),self.MenuBTN,text='OPTIONS',fn='self.new(3)',thickness = 2),
							BTN(self.win,0,(840,550,300,100),self.MenuBTN,text='QUIT',fn='self.playing = 0',thickness = 2)]]
			#Insert moving character sprites(just the heads) in BG from sprites_folder
			#Add transparency to it
		
		if location == 1:
			self.font_LL = pygame.font.SysFont('Comic Sans MS',48)
			self.font_L = pygame.font.SysFont('Comic Sans MS',32)
			self.font_M = pygame.font.SysFont('Comic Sans MS',16)
			self.font_S = pygame.font.SysFont('Comic Sans MS',8)
			#Title Text
			self.text = self.font_LL.render('Choose your character',True,BLACK)
			self.text_rect = self.text.get_rect(center=(640,50))
			self.img.append([self.text,self.text_rect])
			#Player Boxes
			for h,i in enumerate(self.joysticks):
				surf = pygame.Surface((200,300))
				pygame.draw.rect(surf,(RED, BLUE, YELLOW, GREEN)[i.get_id()],(0,0,200,300))
				surf.blit(self.font_L.render('PLAYER '+str(h+1),True,BLACK),(5,140))
				pygame.draw.rect(surf,BLACK,(0,0,200,300),2)
				pygame.draw.rect(surf,GRAEY,(5,5,140,140))
				pygame.draw.rect(surf,GRAEY,(30,185,150,20))
				pygame.draw.rect(surf,GRAEY,(30,225,150,20))
				pygame.draw.rect(surf,GRAEY,(30,265,150,20))
				pygame.draw.circle(surf,GRAY,(20,195),15)
				pygame.draw.circle(surf,BLACK,(20,195),15,1)
				pygame.draw.circle(surf,GRAY,(20,235),15)
				pygame.draw.circle(surf,BLACK,(20,235),15,1)
				pygame.draw.circle(surf,GRAY,(20,275),15)
				pygame.draw.circle(surf,BLACK,(20,275),15,1)
				surf.blit(self.icons['attack'],(12,187))
				surf.blit(self.icons['defense'],(12,227))
				surf.blit(self.icons['speed'],(12,267))
				self.img.append([surf,((96*(h+1))+(200*h),400)])
				#Put user select box here.
				#Selected chars stats, sprite, class etc.
			temp = []
			for j,k in enumerate(sorted(self.char_sprites)):
				temp.append(BTN(self.win,0,(40+100*(j%12),100+100*(j//12),100,100),self.MenuBTN,text=k,allign = 'bottom',image = pygame.transform.scale(self.char_sprites[k][0],(100,100))))
				if j%12 == 0 and j != 0:
					self.BTN_list.append(temp)
					temp = []
			if temp != []:
				self.BTN_list.append(temp)
				temp = []

	def load_data(self):
		game_folder = os.path.dirname(__file__)
		map_folder = os.path.join(game_folder, 'maps')
		img_folder = os.path.join(game_folder, 'images')
		self.sprites_folder = os.path.join(img_folder, 'sprites')
		bg_folder = os.path.join(img_folder,'backgrounds')
		icon_folder = os.path.join(img_folder,'icon')
		self.char_sprites = {}
		self.maps = {}
		self.covers = {}
		self.icons = {}

		for filename in os.listdir(map_folder): #Load Map
			if filename.endswith(".pfmap"):self.maps[filename[:-6]] = zipfile.ZipFile(os.path.join(map_folder, filename))
		for x in self.maps:
			self.covers[x] = pygame.image.load(BytesIO(self.maps[x].read("cover.png")))

		for fileName in os.listdir(self.sprites_folder): #Load Character sprites
			file = os.path.join(self.sprites_folder, fileName)
			for i in sorted(os.listdir(file)):
				if i.lower().endswith(".png") or i.lower().endswith(".jpg"):
					sprite_image = pygame.image.load(os.path.join(file,i)).convert_alpha()
					head_rect = (285,80,70,70)
					head = pygame.transform.scale(sprite_image.subsurface(head_rect),(int(70*(0.3)),int(70*0.3)))
					head.set_colorkey((192,192,192))
					self.char_sprites[str(fileName).strip('.png')] = [head,self.sprite_data]
				elif i.lower().endswith(".trash"):
					self.sprite_data = open(os.path.join(file,i)).readline()

		for fileName in os.listdir(bg_folder): #Load BG image
			if fileName == 'menu.png' or fileName == 'menu.jpg':
				self.bg = pygame.transform.scale(pygame.image.load(os.path.join(bg_folder,fileName)).convert_alpha(),RES)
		
		for fileName in os.listdir(icon_folder):
			self.icons[fileName[:-4]] = pygame.transform.scale(pygame.image.load(os.path.join(icon_folder,fileName)).convert_alpha(),(16,16))
			self.icons[fileName[:-4]].set_colorkey((255,255,255))

	def run(self):
		self.playing = 1
		while self.playing:
			try:[x.update() for x in self.joysticks]
			except:()
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.mDown = 1
				else:
					self.mDown = 0
			self.draw()
			self.buttons()
			pygame.display.update()

	def buttons(self):
		for i in self.MenuBTN:
			if i.rect.collidepoint(pygame.mouse.get_pos()):
				i.update(mOver=1)
				if self.mDown:
					exec(i.fn)
					if i.clickable:
						for j in self.MenuBTN:
							j.update(clicked = 0)
						i.update(clicked = 1)
			else:
				i.update()

	def draw(self):
		for i in self.img:
			self.win.blit(i[0],i[1])

	def run_paint(self):
		p = paint(self.win,self.sprites_folder)
		p.new()
		p.run()
		self.playing = p.running


pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for x in joysticks: x.init()
for x in joysticks[:]:
	try: #incompatible controller detection
		for i in (0,1): x.get_axis(i) #remove controllers with no thumbstick
		if "ppjoy" in x.get_name().lower():0/0 #remove faked controllers (steering wheels, flight sticks, etc)
		if "rvl"   in x.get_name().lower():0/0 #remove wii controllers
	except:joysticks.pop(joysticks.index(x)).quit()
if len(joysticks) < 4: joysticks.append(dummyJoystick(len(joysticks)))
else: joysticks=joysticks[:4]
#win = pygame.display.set_mode((1280,720), pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
win = pygame.display.set_mode(RES)

g = GUI(win,joysticks)
g.new(0)
g.run()
pygame.quit()
