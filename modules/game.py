import pygame, math, os, zipfile, sys
from io import BytesIO
from modules.character import *
from chars import *
from modules.map import *
from modules.joystick_wrapper import *
from settings import *

class Game():
	def __init__(self, win, joysticks, map="default", charList = [],platform = None, sounds = None):
		self.joysticks = joysticks
		self.win = win
		self.charList = charList
		self.platform = platform
		self.Sounds = sounds
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()#Sprite Groups
		self.ground = pygame.sprite.Group()
		self.objects = pygame.sprite.Group()
		self.map = map
		self.once = 1
		self.ranks = []#Stores what place the characters are (eg. 1st, 2nd)
	def new(self):
		self.loadData()
		self.HPFont = pygame.font.SysFont("Trebuchet MS",36)
		self.NameFont = pygame.font.SysFont("Constantia",18)
		self.TinyFont = pygame.font.SysFont("Constantia",12)
		if self.charList == []:
			for x in self.joysticks:
				if "ouya" in x.get_name().lower(): mage.char(self, x, 'test',[0,3,1,2,4,5])
				elif "xbox" in x.get_name().lower(): shooter.char(self, x, 'test')
				else: друг.char(self, x, 'test')
				#Classes:
				#	Mage
				#	друг
				#	Shooter
		else:
			for x,y in enumerate(self.charList):
				#x is num
				#y is values
				if "ouya" in self.joysticks[x].get_name().lower():
					exec(str(['mage','друг','shooter','brawler'][y[0]])+'.char(self,self.joysticks[x],y[1],[0,3,1,2,4,5])')
				else:
					exec(str(['mage','друг','shooter','brawler'][y[0]])+'.char(self,self.joysticks[x],y[1])')
		#load map
		for x in self.maps[self.map].open("map").readlines():
			if x.strip():
				file = x.decode("UTF-8").strip().split()
				texture = pygame.image.load(BytesIO(self.maps[self.map].read(file[-1])))
				file = [file[0]]+list(map(int,file[1:-1]))
				if file[0] == "g": Ground(self, file[1:5], texture=texture)
				if file[0] == "p": Ground(self, file[1:5], 1, texture=texture)
				if file[0] == "m": Moving(self, file[1:5], file[5], file[6], file[7:9], texture=texture)
		try:
			pygame.mixer.music.load(BytesIO(self.maps[self.map].read("music.ogg")))
			pygame.mixer.music.play(-1)
		except:()
		try: self.bg = pygame.transform.smoothscale(pygame.image.load(BytesIO(self.maps[self.map].read("bg.png"))), (RES[0], RES[1])).convert()
		except: self.bg=0
	def loadData(self):
		game_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
		map_folder = os.path.join(game_folder, 'maps')
		img_folder = os.path.join(game_folder, 'images')
		effect_folder = os.path.join(img_folder, 'effects')
		sprites_folder = os.path.join(img_folder, 'sprites')
		self.effects = {}
		self.char_sprites = {}
		self.maps = {}
		for filename in os.listdir(map_folder): #Load Map
			if filename.endswith(".pfmap"):self.maps[filename[:-6]] = zipfile.ZipFile(os.path.join(map_folder, filename))
		for fileName in os.listdir(effect_folder): #Load effects
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
		for fileName in os.listdir(sprites_folder): #Load Character sprites
			file = os.path.join(sprites_folder, fileName)
			for i in sorted(os.listdir(file)):
				if i.lower().endswith(".png") or i.lower().endswith(".jpg"):
					sprite_image = pygame.image.load(os.path.join(file,i)).convert()
					#Splits up character into different subsurfaces
					head_rect = (285,80,70,70)
					torso_rect = (250,150,140,180)
					L_arm_rect = (150,180,100,50)
					L_hand_rect = (100,180,50,50)
					R_arm_rect = (390,180,100,50)
					R_hand_rect = (490,180,50,50)
					L_leg_rect = (250,330,50,100)
					L_foot_rect = (250,430,50,50)
					R_leg_rect = (340,330,50,100)
					R_foot_rect = (340,430,50,50)
					head = pygame.transform.scale(sprite_image.subsurface(head_rect),(int(70*(0.3)),int(70*0.3)))
					head.set_colorkey((192,192,192))
					torso = pygame.transform.scale(sprite_image.subsurface(torso_rect),(int(140*(0.3)),int(180*0.3)))
					torso.set_colorkey((192,192,192))
					L_arm = pygame.transform.scale(sprite_image.subsurface(L_arm_rect),(int(100*(0.3)),int(50*0.3)))
					L_arm.set_colorkey((192,192,192))
					L_hand = pygame.transform.scale(sprite_image.subsurface(L_hand_rect),(int(50*(0.3)),int(50*0.3)))
					L_hand.set_colorkey((192,192,192))
					R_arm = pygame.transform.scale(sprite_image.subsurface(R_arm_rect),(int(100*(0.3)),int(50*0.3)))
					R_arm.set_colorkey((192,192,192))
					R_hand = pygame.transform.scale(sprite_image.subsurface(R_hand_rect),(int(50*(0.3)),int(50*0.3)))
					R_hand.set_colorkey((192,192,192))
					L_leg = pygame.transform.scale(sprite_image.subsurface(L_leg_rect),(int(50*(0.3)),int(100*0.3)))
					L_leg.set_colorkey((192,192,192))
					L_foot = pygame.transform.scale(sprite_image.subsurface(L_foot_rect),(int(50*(0.3)),int(50*0.3)))
					L_foot.set_colorkey((192,192,192))
					R_leg = pygame.transform.scale(sprite_image.subsurface(R_leg_rect),(int(50*(0.3)),int(100*0.3)))
					R_leg.set_colorkey((192,192,192))
					R_foot = pygame.transform.scale(sprite_image.subsurface(R_foot_rect),(int(50*(0.3)),int(50*0.3)))
					R_foot.set_colorkey((192,192,192))
					self.char_sprites[str(fileName).strip('.png')] = [head,torso,L_arm,L_hand,R_arm,R_hand,L_leg,L_foot,R_leg,R_foot,self.sprite_data]
				elif i.lower().endswith(".trash"):
					self.sprite_data = open(os.path.join(file,i)).readline()
	def run(self):
		self.playing = 1#Game is running
		self.running = 1#Program is running
		self.Sounds.play('ready')
		self.counter = self.clock.get_time()
		while self.playing:
			keys = pygame.key.get_pressed()
			events = pygame.event.get()
			for x in self.joysticks: #generate button press events for dummy joysticks
				try:x.update(events)
				except:pass
			self.dt = self.clock.tick(FPS) / 1000
			self.counter += self.dt
			if self.counter > 3 and self.once:
				self.once = 0
				self.Sounds.play('GO')
			#Events
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0;self.running = 0;pygame.mixer.stop();pygame.mixer.music.\
					stop() #hammertime!
				if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE: self.playing=0;pygame.mixer.stop();pygame.mixer.music.stop()
			if self.bg: self.win.blit(self.bg,(0,0))
			else:self.win.fill(WHITE)
			self.objects.update()
			self.sprites.update(keys, events)
			self.ground.update()
			self.draw()
			left = [x for x in self.sprites if x.stock > 0]
			if len(left)<= 1:
				self.playing = 0
				self.ranks = sorted([x for x in self.sprites], key=lambda x:x.dead) #sort players by time of death (breaks if game is played before jan 1 1970, or after jan 19 2038 on 32 bit systems)
				print(self.ranks)
				if min(self.ranks, key=lambda x:x.dead).dead==0:self.ranks=[self.ranks[0]]+self.ranks[1:][::-1]
				print(self.ranks)
				pygame.mixer.stop()
				pygame.mixer.music.stop()

	def draw(self):
		pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		for j in self.sprites:
			i = j.joystick.get_id()
			img = pygame.transform.scale(j.sprite_image[0].copy(),(80,80))
			img_s = pygame.transform.scale(j.sprite_image[0].copy(),(20,20))
			pygame.draw.rect(self.win,(BLUE,RED,YELLOW,GREEN)[i],(96*(i+1)+(200*i),600,200,100))
			pygame.draw.rect(self.win,BLACK,(96*(i+1)+(200*i),600,200,100),4)
			self.win.blit(img,(96*(i+1)+(200*i)+5,600+5))
			name = self.NameFont.render(str(j.name),True,BLACK)
			self.win.blit(name,name.get_rect(center=(96*(i+1)+(200*i)+50,690)))
			if j.stock:
				dmg = j.dmg
				dmg_color = (max(int(255-(bool(dmg//180)*(dmg-180))),180),#RED
							max(int(255-(bool(dmg//60)*(dmg-60))*1.875),0),#GREEN
							max(int(255-(j.dmg*4.25)),0))#BLUE
				dmg_txt_c = self.HPFont.render(str(int(dmg))+'%',True,dmg_color)
				for k in [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]:
					outline = self.HPFont.render(str(int(dmg))+'%',True,BLACK)
					rect = outline.get_rect(center=(96*(i+1)+(200*i)+150+(k[0]*2),670+(k[1]*2)))
					self.win.blit(outline,rect)
				stock_label = self.TinyFont.render('Stocks Left',True,BLACK)
				self.win.blit(stock_label,(96*(i+1)+(200*i)+100,605))
				pygame.draw.line(self.win,BLACK,(96*(i+1)+(200*i)+100,617),(96*(i+1)+(200*i)+160,617),2)
				for l in range(j.stock):
					self.win.blit(img_s,(96*(i+1)+(200*i)+100+(25*l),620))
				self.win.blit(dmg_txt_c,dmg_txt_c.get_rect(center=(96*(i+1)+(200*i)+150,670)))
		pygame.display.update()

if __name__ == "__main__":
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
#	win = pygame.display.set_mode((1280,720), pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
	win = pygame.display.set_mode((1280,720))

	g = Game(win, joysticks, "default")
	g.new()
	g.run()
	pygame.quit()