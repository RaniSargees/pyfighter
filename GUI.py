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
		self.pos = (0,0)
		#Location Index:
		#	0, Main Menu
		#	1, Character Select
		#	2, Map Select
		#	3, Options

	def new(self,location=0):
		self.buttons = pygame.sprite.Group()
		self.image = []
		if location == 0: #Main Menu
			self.load_data()
			self.img.append([self.bg,(0,0)]) #Background image
			#Title Text
			self.font = pygame.font.SysFont('Comic Sans MS',144)
			self.text = self.font.render('PYFIGHTER',True,BLACK)
			self.text_rect = self.text.get_rect(center=(640,180))
			self.img.append([self.text,self.text_rect])
			#Buttons
			BTN(self.win,0,(100,300,600,200),self.buttons,text='PLAY',fn='self.new(1)',thickness = 4)
			BTN(self.win,0,(800,300,300,200),self.buttons,text='CREATE')
			
			#Insert moving character sprites(just the heads) in BG from sprites_folder
			#Add transparency to it
	
	def load_data(self):
		game_folder = os.path.dirname(__file__)
		map_folder = os.path.join(game_folder, 'maps')
		img_folder = os.path.join(game_folder, 'images')
		sprites_folder = os.path.join(img_folder, 'sprites')
		bg_folder = os.path.join(img_folder,'backgrounds')
		self.char_sprites = {}
		self.maps = {}
		self.covers = {}
		
		for filename in os.listdir(map_folder): #Load Map
			if filename.endswith(".pfmap"):self.maps[filename[:-6]] = zipfile.ZipFile(os.path.join(map_folder, filename))
		
		for x in self.maps:
			self.covers[x] = pygame.image.load(BytesIO(self.maps[x].read("cover.png")))
			
		for fileName in os.listdir(sprites_folder): #Load Character Faces
			sprite_image = pygame.image.load(os.path.join(sprites_folder,fileName)).convert_alpha()
			head_rect = (285,80,70,70)
			head = pygame.transform.scale(sprite_image.subsurface(head_rect),(int(70*(0.3)),int(70*0.3)))
			head.set_colorkey((192,192,192))
			self.char_sprites[str(fileName).strip('.png')] = head
		
		for fileName in os.listdir(bg_folder):
			if fileName == 'menu.png' or fileName == 'menu.jpg':
				self.bg = pygame.transform.scale(pygame.image.load(os.path.join(bg_folder,fileName)).convert_alpha(),RES)
		
	def run(self):
		self.playing = 1
		while self.playing:
			events = pygame.event.get()
			self.draw()
			pygame.display.update()
			
			
	
	def draw(self):
		for i in self.img:
			self.win.blit(i[0],i[1])
		self.buttons.update()
			
	
	
	

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













