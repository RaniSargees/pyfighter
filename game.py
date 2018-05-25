import pygame, math, os, zipfile
from io import BytesIO
from characters import *
from map import *
from joystick_wrapper import *
from settings import *

class Game():
	def __init__(self, win, joysticks):
		self.joysticks = joysticks
		self.win = win
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
		self.ground = pygame.sprite.Group()
		self.objects = pygame.sprite.Group()
	def new(self):
		self.loadData()
		self.TempFont = pygame.font.SysFont("monospace", 36)
		for x in self.joysticks:
			if "ouya" in x.get_name().lower():
				Mage(self, x, [0,3,1,2,4,5])
			else:
				Mage(self, x)
		#load default map
		for x in self.maps["default"].open("map").readlines():
			if x.strip():
				file = x.decode("UTF-8").strip().split()
				texture = pygame.image.load(BytesIO(self.maps["default"].read(file[-1])))
				file = [file[0]]+list(map(int,file[1:-1]))
				if file[0] == "g": Ground(self, file[1:5], texture=texture)
				if file[0] == "p": Ground(self, file[1:5], 1, texture=texture)
				if file[0] == "m": Moving(self, file[1:5], file[5], file[6], file[7:9], texture=texture)
	def loadData(self):
		game_folder = os.path.dirname(__file__)
		map_folder = os.path.join(game_folder, 'maps')
		img_folder = os.path.join(game_folder, 'images')
		effect_folder = os.path.join(img_folder, 'effects')
		self.effects = {}
		self.maps = {}
		for filename in os.listdir(map_folder):
			if filename.endswith(".pfmap"):self.maps[filename[:-6]] = zipfile.ZipFile(os.path.join(map_folder, filename))
		for fileName in os.listdir(effect_folder):
			file = os.path.join(effect_folder, fileName)
			temp = []
			for i in sorted(os.listdir(file)):
				if i.lower().endswith(".txt"):
					key = list(map(int,open(os.path.join(file,i)).readline().split(',')))
				if i.lower().endswith(".jpg") or i.lower().endswith(".png"):
					var = (pygame.image.load(os.path.join(file,i)).convert())
					var.set_colorkey(key)
					temp.append(var)
			self.effects[str(fileName)] = temp
	def run(self):
		self.playing = 1
		while self.playing:
			keys = pygame.key.get_pressed()
			events = pygame.event.get()
			for x in self.joysticks: #generate button press events for dummy joysticks
				try:x.update(events)
				except:pass
			self.dt = self.clock.tick(FPS) / 1000
			#Events
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE: self.playing=0
			self.win.fill(WHITE)
			self.objects.update()
			self.sprites.update(keys, events)
			self.ground.update()
			self.draw()

	def draw(self):
		pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		for i,j in enumerate(self.sprites):
			self.win.blit(self.TempFont.render(str(int(j.dmg)),True,(RED, GREEN, BLUE, WHITE)[j.joystick.get_id()]),((200*i)+50,650))
		pygame.display.update()


pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for x in joysticks: x.init()
if len(joysticks) < 4: joysticks.append(dummyJoystick(len(joysticks)))
#win = pygame.display.set_mode((1280,720), pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
win = pygame.display.set_mode(RES)

g = Game(win, joysticks)
g.new()
g.run()
pygame.quit()

