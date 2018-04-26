import pygame, math
from Characters import *
FPS = 60

class Game():
	def __init__(self):
		pygame.init()
		self.win = pygame.display.set_mode((1280,720))
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
		self.ground = 500
	def new(self):
		self.Test = Char(self)
	def run(self):
		self.playing = 1
		while self.playing:
			keys = pygame.key.get_pressed()
			events = pygame.event.get()
			self.dt = self.clock.tick(FPS) / 1000
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
