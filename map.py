import pygame
from settings import *

class Ground(pygame.sprite.Sprite):
	def __init__(self, game, rect, platform = 0):
		self.rect = rect
		self.game = game
		self.platform = platform
		pygame.sprite.Sprite.__init__(self, game.ground)
	def update(self):
		pygame.draw.rect(self.game.win, BLACK, self.rect)
