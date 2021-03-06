#		GUI
#Displays main menu for game
#Can be controlled using mouse or controller
#Loads Game and Paint programs
import pygame, os, zipfile, math, sys
from modules.paint import *
from modules.game import *
from modules.Sound_Loader import *
from settings import *
from modules.joystick_wrapper import *
from modules.map import *
from modules.BTN import *

class GUI():
	def __init__(self,win,joysticks):#init variables
		self.win = win
		self.joysticks = joysticks
		self.bg = None
		self.img = []
		self.Sounds = Sound_Manager()
		self.Sounds.load_music('menu')
		pygame.mixer.music.play(-1)
		self.mDown = 0
		self.fade = 1
		self.fade_dir = 0
		self.map_pos = 0
		self.BTN_list = []#List of buttons in a scene
		self.action = 0
		self.counter = 0
		#variables used to run stuff only once
		self.once = 1
		self.once2= 1
		self.once3= 1
		self.dt = 0
		self.time = pygame.time.Clock()
		self.pointer = [] #Where the joystick is current pointing to
		self.pointerUpdate = [] #Prevents pointer from changing rapidly (Must let axis go before pointer can be moved again)
		self.joystick_button = [] #The button that is pressed (default to -1)
		self.joystick_selected = [] #If the joystick has selected something lock it
		self.char_selected = [] #The character currently selected by the controller
		self.char_name = [] #Name of the character selected (the name used to load the character in)
		self.once_char = [1] #To make stuff only run once
		for x in joysticks[:-1]:
			self.once_char.append(1)
			self.pointer.append([0,0])
			self.pointerUpdate.append(0)
			self.joystick_button.append(-1)
			self.joystick_selected.append(0)
			self.char_selected.append(None)
			self.char_name.append(None)
		self.char_selected.append(None)
		self.char_name.append(None)

		#Fonts
		self.font_LLL = pygame.font.SysFont('Comic Sans MS',72)
		self.font_LL = pygame.font.SysFont('Comic Sans MS',48)
		self.font_L = pygame.font.SysFont('Comic Sans MS',32)
		self.font_M = pygame.font.SysFont('Comic Sans MS',16)
		self.font_S = pygame.font.SysFont('Comic Sans MS',8)

	def new(self,location=0):
		#Location Index:
		#   0, Main Menu
		#   1, Character Select
		#   2, Map Select
		#   3, Options
		self.location = location
		self.load_data()
		self.MenuBTN = pygame.sprite.Group()
		self.img = []
		self.BTN_list = []
		self.img.append([self.bg,(0,0)]) #Background image
		self.reset_pointers()#Resets all controller positions on screen

		if self.location == 0: #Main Menu
			#Title Text
			self.font = pygame.font.SysFont('Comic Sans MS',144)
			self.text = self.font.render('PYFIGHTER',True,BLACK)
			self.text_rect = self.text.get_rect(center=(640,180))
			self.img.append([self.text,self.text_rect])
			#Buttons
			self.BTN_list = [[BTN(self.win,0,(140,300,600,200),self.MenuBTN,text='PLAY',fn='self.new(1)',thickness = 2,clickable = False),
							BTN(self.win,0,(840,300,300,200),self.MenuBTN,text='CREATE',fn='self.run_paint()',thickness = 2,clickable = False)],
							[BTN(self.win,0,(140,550,600,100),self.MenuBTN,text='RECONNECT CONTROLLERS',fn='self.new(3)',thickness = 2,clickable = False),
							BTN(self.win,0,(840,550,300,100),self.MenuBTN,text='QUIT',fn='self.playing = 0',thickness = 2,clickable = False)]]
		elif self.location == 1: #Character Select screen
			self.Sounds.play("choose")#Play announcer sound 
			#Back Button
			self.BTN_list = [[BTN(self.win,0,(5,5,200,60),self.MenuBTN,text='Back to Menu',fn='self.new(0)', clickable = False)]]
			#Title Text
			self.text = self.font_LL.render('Choose your character',True,BLACK)
			self.text_rect = self.text.get_rect(center=(640,50))
			self.img.append([self.text,self.text_rect])
			for h,i in enumerate(self.joysticks): #Player Boxes
				surf = pygame.Surface((200,300))
				pygame.draw.rect(surf,(BLUE,RED,YELLOW, GREEN)[i.get_id()],(0,0,200,300))
				surf.blit(self.font_L.render('PLAYER '+str(h+1),True,BLACK),(5,140))
				pygame.draw.rect(surf,BLACK,(0,0,200,300),2)
				pygame.draw.rect(surf,GRAEY,(5,5,140,140))
				pygame.draw.rect(surf,GRAEY,(35,185,154,20))
				pygame.draw.rect(surf,GRAEY,(35,225,154,20))
				pygame.draw.rect(surf,GRAEY,(35,265,154,20))
				pygame.draw.circle(surf,GRAY,(20,195),15)
				pygame.draw.circle(surf,BLACK,(20,195),15,1)
				pygame.draw.circle(surf,GRAY,(20,235),15)
				pygame.draw.circle(surf,BLACK,(20,235),15,1)
				pygame.draw.circle(surf,GRAY,(20,275),15)
				pygame.draw.circle(surf,BLACK,(20,275),15,1)
				surf.blit(pygame.transform.scale(self.icons['attack'].copy(),(16,16)),(12,187))
				surf.blit(pygame.transform.scale(self.icons['defense'].copy(),(16,16)),(12,227))
				surf.blit(pygame.transform.scale(self.icons['speed'].copy(),(16,16)),(12,267))
				self.img.append([surf,((96*(h+1))+(200*h),400)])
			temp = []
			char_amount = len(self.char_sprites)
			size_reduction = 0
			while char_amount > (12+(size_reduction*6))*(size_reduction+2): #Determines how large each character profile is on the character select screen
				size_reduction += 1
			profile_size = (200/(size_reduction+2))
			for j,k in enumerate(sorted(self.char_sprites, key=lambda k:k.lower())):
				if j%(12+(size_reduction*6)) == 0 and j != 0:
					self.BTN_list.append(temp)
					temp = []
				temp.append(BTN(self.win,0,(40+profile_size*(j%(12+(size_reduction*6))),100+profile_size*(j//(12+(size_reduction*6))),profile_size,profile_size),self.MenuBTN,text=k,allign = 'bottom',fn = 'self.char_name[x],self.char_selected[x] = [self.char_sprites["'+str(k)+'"][1],"'+str(k)+'"],self.char_sprites["'+str(k)+'"]',thickness = 2, image = pygame.transform.scale(self.char_sprites[k][0].copy(),(int(profile_size),int(profile_size)))))
			if temp != []:
				self.BTN_list.append(temp)
				temp = []
		elif self.location == 2: #Map select screen
			self.text = self.font_LLL.render('Select your map',True,BLACK)
			self.img.append([self.text,self.text.get_rect(center=(640,40))])
			#Selection buttons
			self.BTN_list = [[BTN(self.win,0,(5,5,200,60),self.MenuBTN,text='Back to Menu',fn='self.new(1)', clickable = False)],#Return to character select screen
							[BTN(self.win,0,(200,200,50,200),self.MenuBTN,text='<',fn='self.map_pos-=1',clickable = False),#Change selected map 
							BTN(self.win,0,(1030,200,50,200),self.MenuBTN,text='>',fn='self.map_pos+=1',clickable = False)],#Change selected map
							[BTN(self.win,8,(540,600,200,100),self.MenuBTN,text='GO',fn='self.run_game()',clickable = False)]]#Start game with selected map
		elif self.location == 3: #Controller Connection
			self.text = self.font_LLL.render('Connect your controllers',True,BLACK)
			self.img.append([self.text,self.text.get_rect(center=(640,80))])
			self.BTN_list = [[BTN(self.win,0,(5,5,200,60),self.MenuBTN,text='Back to Menu',fn='self.new(0)', clickable = False)],#Back to main menu
							[BTN(self.win,0,(390,500,500,100),self.MenuBTN,text='Reset Controllers',fn='self.new_joystick()', clickable = False)]]#Reconnect all joysticks
			surf = pygame.Surface((1280,300),pygame.SRCALPHA,32)
			for i in range(4):
				pygame.draw.rect(surf,(BLUE,RED,YELLOW, GREEN)[i],(96*(i+1)+200*i,0,200,300))
				pygame.draw.rect(surf,BLACK,(96*(i+1)+200*i,0,200,300),3)
			self.img.append([surf,(0,160)])
			for i in range(4):
				text = self.font_LLL.render('P '+str(i+1),True,BLACK)
				self.img.append([text,text.get_rect(center=(100+(96*(i+1)+200*i),210))])
		elif self.location == 4:#Win/End of game screen
			self.text = self.font_LLL.render("THE WINNER IS: "+str(self.ranks[0].name).upper(),1,BLACK)
			self.img.append([self.text,(220,5)])
			self.BTN_list = [[BTN(self.win,0,(5,5,200,60),self.MenuBTN,text='Back to Menu',fn='self.new(1)', clickable = False)]]
			surf = pygame.Surface((1280,560),pygame.SRCALPHA,32)
			temp = []
			for h,i in enumerate(self.ranks):#Loops through the ranks list and places character podium height based on weather if the won or not
				l = i.joystick.get_id()
				pygame.draw.rect(surf,(BLUE,RED,YELLOW, GREEN)[l],(96*(l+1)+200*l,(bool(h)*50),200,420))
				pygame.draw.rect(surf,BLACK,(96*(l+1)+200*l,0+(bool(h)*50),200,430),3)
				rank_text = self.font_LLL.render(('1st','2nd','3rd','4th')[h],True,((255,215,0),(192,192,192),(80,50,20),(70,130,180))[h])#Blit text with their position
				if h == 0:#If they won play DAB animation
					sprite = i.anim.DAB_ON_HATERS()
				else:#If they didn't win play idle animation
					sprite = i.anim.idle()
				self.img.append([pygame.transform.scale(sprite,(int(sprite.get_width()*1.5),int(sprite.get_height()*1.5))),(96*(l+1)+(200*l)-90,(bool(h)*50)-80)])
				for k in [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]]:#Draw text outline (For bold effect)
					outline = self.font_LLL.render(('1st','2nd','3rd','4th')[h],True,BLACK)
					rect = outline.get_rect(center=(96*(l+1)+(200*l)+100+(k[0]),300+(k[1])))
					temp.append([outline,rect])
				temp.append([rank_text,rank_text.get_rect(center=(96*(l+1)+(200*l)+100,300))])
			self.img.append([surf,(0,300)])
			for i in range(len(self.ranks)):#Draws what player they are
				text = self.font_LLL.render('P '+str(i+1),True,BLACK)
				self.img.append([text,text.get_rect(center=(100+(96*(i+1)+200*i),380))])
			self.img.extend(temp)
			[x.kill() for x in self.ranks]



	def reset_pointers(self,char_name = 0):#Resets all controller pointer
		self.pointer = []
		self.pointerUpdate = []
		self.joystick_button = []
		self.joystick_selected = []
		self.char_selected = []
		self.once_char = [1]
		if char_name == 1:
			self.char_name = [None]
		for x in self.joysticks[:-1]:	
			self.once_char.append(1)
			self.pointer.append([0,0])
			self.pointerUpdate.append(0)
			self.joystick_button.append(-1)
			self.joystick_selected.append(0)
			self.char_selected.append(None)
			if char_name ==1:
				self.char_name.append(None)
		self.char_selected.append(None)

	def load_data(self):
		#Loads in all required data
		game_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
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
			self.icons[fileName[:-4]] = pygame.image.load(os.path.join(icon_folder,fileName)).convert_alpha()
			self.icons[fileName[:-4]].set_colorkey(WHITE)

	def run(self):
		self.playing = 1
		while self.playing:
			events = pygame.event.get()
			try:[x.update(events) for x in self.joysticks]
			except:()
			#User events
			self.mDown = 0
			for event in events:
				if event.type == pygame.JOYBUTTONDOWN:
					try:self.joystick_button[event.joy] = event.button
					except: pass
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.mDown = 1
			self.draw()
			if self.BTN_list != []:
				self.pointers()
				self.buttons()
			self.dt = self.time.tick(60)/1000#Delta Time (max 60fps)
			pygame.display.update()

	def pointers(self):
		for x in self.joysticks[:-1]:#Updates pointers based on controller movement. It also limits controller selection to stay within BTN_list
			if not(self.pointerUpdate[x.get_id()]) and not(self.joystick_selected[x.get_id()]):
				y = x.get_id()
				if x.get_axis(0) < -.7:
					self.pointerUpdate[x.get_id()] = 1
					self.pointer[y] = [max(self.pointer[y][0]-1,0),self.pointer[y][1]]
				elif x.get_axis(0) > .7:
					self.pointerUpdate[x.get_id()] = 1
					self.pointer[y] = [min(self.pointer[y][0]+1,len(self.BTN_list[self.pointer[y][1]])-1),self.pointer[y][1]]
				if x.get_axis(1) > .7:
					self.pointerUpdate[x.get_id()] = 1
					self.pointer[y] = [self.pointer[y][0],min(self.pointer[y][1]+1,len(self.BTN_list)-1)]
					self.pointer[y] = [max(min(self.pointer[y][0],len(self.BTN_list[self.pointer[y][1]])-1),0),self.pointer[y][1]]
				elif x.get_axis(1) < -.7:
					self.pointerUpdate[x.get_id()] = 1
					self.pointer[y] = [self.pointer[y][0],max(self.pointer[y][1]-1,0)]
					self.pointer[y] = [max(min(self.pointer[y][0],len(self.BTN_list[self.pointer[y][1]])-1),0),self.pointer[y][1]]

			elif abs(x.get_axis(0)) < .7 and abs(x.get_axis(1)) < .7:
				self.pointerUpdate[x.get_id()] = 0

		for x,y in enumerate(self.joystick_button):#If the controller pressed the select button run the function of the pressed button
			button = self.BTN_list[self.pointer[x][1]][self.pointer[x][0]]
			self.joystick_button[x] = -1
			if y == 0:
				self.Sounds.play('click')
				exec(button.fn)
				if button.clickable:
					self.joystick_selected[self.joysticks[x].get_id()] = 1
					button.update(clicked =1,hColor = (BLUE,RED,YELLOW,GREEN)[self.joysticks[x].get_id()])
			if y == 1:
				self.joystick_selected[self.joysticks[x].get_id()] = 0
				button.update(clicked = 0)
				self.char_selected[x] = None


	def buttons(self):
		for i in self.MenuBTN:#If the mouse selects and clicked a button run its function
			if i.rect.collidepoint(pygame.mouse.get_pos()):
				i.update(mOver=1,hColor=(BLUE,RED, YELLOW, GREEN)[self.joysticks[-1].get_id()])
				if self.mDown:
					x = -1
					self.Sounds.play('click')
					self.once_char[x] = 1
					exec(i.fn)
					if i.clickable:
						for j in self.MenuBTN:
							j.update(clicked = 0)
						i.update(clicked = 1,hColor=(BLUE,RED, YELLOW, GREEN)[self.joysticks[-1].get_id()])
			else:
				i.update()
		for i,j in enumerate(self.pointer):
			x = j[0]
			y = j[1]
			self.BTN_list[y][x].update(mOver=1,hColor=(BLUE,RED, YELLOW, GREEN)[i])

	def draw(self):
		for i in self.img: #Prints all images in the self.img list
			self.win.blit(i[0],i[1])
		if self.location == 1:#Character Select Screen
			for i,j in enumerate(self.char_selected): #If a character is selected blit its image and stats onto the user profile
				if j != None:
					self.win.blit(pygame.transform.scale(j[0].copy(),(140,140)),((96*(i+1))+(200*i)+5,405))
					stats = list(map(int,j[1].replace('[','').replace(']','').split(',')))
					class_name = pygame.transform.rotate(self.font_L.render(('Mage','друг','Shooter','Brawler')[stats[0]],True,BLACK),90)
					class_name_rect = class_name.get_rect(center=(173+(96*(i+1))+(200*i),472))
					self.win.blit(class_name,class_name_rect)
					if self.once_char[i]:
						self.once_char[i] = 0
						self.Sounds.play(('mage','apyr','shooter','brawler')[stats[0]])#Play sound effect if that char is selected
					#Draws charcter stats
					for k in range(stats[1]):
						pygame.draw.rect(self.win,GREEN,(35+(96*(i+1))+(200*i)+(14*k),585,14,20))

					for l in range(stats[2]):
						pygame.draw.rect(self.win,GREEN,(35+(96*(i+1))+(200*i)+(14*l),625,14,20))

					for m in range(stats[3]):
						pygame.draw.rect(self.win,GREEN,(35+(96*(i+1))+(200*i)+(14*m),665,14,20))
				else:
					self.once_char[i] = 1
				for n in range(11):#Draw outline for character stats
					pygame.draw.rect(self.win,BLACK,(35+(96*(i+1))+(200*i)+(14*n),585,14,20),2)
					pygame.draw.rect(self.win,BLACK,(35+(96*(i+1))+(200*i)+(14*n),625,14,20),2)
					pygame.draw.rect(self.win,BLACK,(35+(96*(i+1))+(200*i)+(14*n),665,14,20),2)
			if len([x for x in self.char_selected if x != None]) == len(self.char_selected) and len(self.char_selected) >= 1:
				if self.once:
					self.once = 0
					self.Sounds.play('slash')
				self.fade_dir += 1
				self.fade = -98*math.cos(math.radians(self.fade_dir%360)) + 98
				pygame.draw.rect(self.win,(255,self.fade,0),(0,310,1280,80))
				text = self.font_LLL.render('Press the Select button to continue',True,BLACK)
				self.win.blit(text,text.get_rect(center=(640,350)))
				if bool(len([x for x in self.joystick_button if x == 0])) or (pygame.Rect(0,310,1280,80).collidepoint(pygame.mouse.get_pos()) and self.mDown):
					self.new(2)
			else:
				self.once = 1
		elif self.location == 2:#Map Select Screen
			if self.map_pos >= len(self.covers):#Prevents the selected map to go beyond list of maps
				self.map_pos = 0
			elif self.map_pos < 0:
				self.map_pos = len(self.covers)-1
			self.win.blit(pygame.transform.scale(self.covers[sorted(self.covers)[self.map_pos]],(740,400)),(270,100))
			text = self.font_LL.render(sorted(self.covers)[self.map_pos],True,BLACK)
			self.win.blit(text,text.get_rect(center=(640,550)))
			pygame.draw.rect(self.win,BLACK,(270,100,740,400),5)

		elif self.location == 3:#Reconnect Controller Screen
			img = pygame.transform.scale(self.icons['controller'],(180,180))
			img2 = pygame.transform.scale(self.icons['keyboard'],(180,180))
			if len(self.joysticks) > 1:
				for i in range(len(self.joysticks[:-1])): #Draws/displays how many controllers are connected
					self.win.blit(img,(10+(96*(i+1)+200*i),240))
				i += 1
				if len(self.joysticks)==4:
					if self.joysticks[-1].get_name() == "Dummy Joystick":
						self.win.blit(img2,(10+(96*(i+1)+200*i),240))
					else:
						self.win.blit(img,(10+(96*(i+1)+200*i),240))
				else:
					self.win.blit(img2,(10+(96*(i+1)+200*i),240))
			else:
				self.win.blit(img2,(10+(96),240))
		
		elif self.location == 4:#Play character sounds of the winner
			self.counter += self.dt
			if self.once3:
				self.Sounds.play('winner')
				self.once3 = 0
				self.counter = 0
			if self.counter > 1.6 and self.once2:
				self.once2 = 0
				self.Sounds.play(('mage','apyr','shooter','brawler')[self.ranks[0].obj_name])



	def run_paint(self):#Runs the paint program
		p = paint(self.win,self.sprites_folder,self.icons)
		p.new()
		p.run()
		self.playing = p.running

	def run_game(self):#Runs the main game
		self.Sounds.stop_all()
		self.once2 = 1
		self.once3 = 1
		self.char_name = [[int(self.char_name[x][0][1]),str(self.char_name[x][1])] for x in range(len(self.char_name))]
		g = Game(self.win,self.joysticks,map=sorted(self.covers)[self.map_pos],charList=self.char_name,platform = self.icons['platform'],sounds = self.Sounds)
		g.new()
		g.run()
		self.playing = g.running
		if not g.ranks:
			self.new(1)
		else:
			self.ranks = g.ranks[:]
			self.new(4)
		self.Sounds.load_music('menu')
		pygame.mixer.music.play(-1)

	def new_joystick(self):#Loads in joysticks
		pygame.joystick.quit()
		pygame.joystick.init()
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
		self.joysticks = joysticks
		self.reset_pointers(1)


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

#Comment and Uncomment lines to have it be full screened or not
#win = pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
win = pygame.display.set_mode(RES)

g = GUI(win,joysticks)
g.new(0)
g.run()
pygame.quit()
