import pygame, math
from Characters import *

class dummyJoystick():
	def __init__(i):pass
	def get_axis(i,j):return 0
	def get_button(i,j):return 0

class Game():
	def __init__(self):
		self.FPS = 60
		pygame.init()
		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		for x in self.joysticks: x.init()
		for x in range(max(4-len(self.joysticks),0)):self.joysticks.append(dummyJoystick())
		self.win = pygame.display.set_mode((1280,720))
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
		self.ground = 500
	def new(self):
		self.Test = Char(self, self.joysticks[0])
	def run(self):
		self.playing = 1
		while self.playing:
			keys = pygame.key.get_pressed()
			events = pygame.event.get()
			self.dt = self.clock.tick(self.FPS) / 1000
			#Events
			for event in events:
				if event.type == pygame.QUIT:
					self.playing = 0
			self.win.fill((255,255,255))
			self.sprites.update(keys, events)
			self.draw()

	def draw(self):
		pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		pygame.display.update()

g = Game()
g.new()
g.run()

