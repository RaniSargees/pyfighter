import pygame, math
from Characters import *
from JoystickWrapper import *
from Settings import *

class Game():
	def __init__(self, win, joysticks):
		self.joysticks = joysticks
		self.win = win
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
		self.ground = 500
	def new(self):
		self.TempFont = pygame.font.SysFont("monospace", 36)
		for x in self.joysticks:
			if "ouya" in x.get_name().lower():
				Char(self, x, [0,1,3,2,4,5])
			else:
				Char(self, x)
	def run(self):
		self.playing = 1
		while self.playing:
			keys = pygame.key.get_pressed()
			events = pygame.event.get()
			for x in self.joysticks: #generate buttonpress events for dummy joysticks
				try:x.update(events)
				except:pass
			self.dt = self.clock.tick(FPS) / 1000
			#Events
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
				if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE: self.playing=0
			self.win.fill(WHITE)
			self.sprites.update(keys, events)
			self.draw()

	def draw(self):
		pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		pygame.draw.rect(self.win, BLACK,(150,572,980,200))
		for i,j in enumerate(self.sprites):
			self.win.blit(self.TempFont.render(str(int(j.dmg)),True,(RED, GREEN, BLUE, WHITE)[j.joystick.get_id()]),((200*i)+50,650))
		pygame.display.update()


pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for x in joysticks: x.init()
if len(joysticks) < 4: joysticks.append(dummyJoystick(len(joysticks)))
win = pygame.display.set_mode((1280,720), pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
#win = pygame.display.set_mode((1280,720))

g = Game(win, joysticks)
g.new()
g.run()
pygame.quit()

