import pygame

class dummyJoystick():
	def __init__(self, left=[pygame.K_a], right=[pygame.K_d], down=[pygame.K_s], up=[pygame.K_w,pygame.K_SPACE],\
	jump=[pygame.K_w,pygame.K_SPACE], heavyatk=[pygame.K_j], lightatk=[pygame.K_k], dodge=[pygame.K_l]):
		self.left = left
		self.right = right
		self.down = down
		self.up = up
		self.jump = jump
		self.heavyatk = heavyatk
		self.lightatk = lightatk
		self.dodge = dodge
		self.buttonstatus = [0 for y in (self.jump, self.heavyatk, self.lightatk, self.dodge)]
		self.oldbuttonstatus = [1 for y in (self.jump, self.heavyatk, self.lightatk, self.dodge)]
	def get_axis(self, axis):
		pressed = pygame.key.get_pressed()
		return -[bool(sum([pressed[x] for x in self.left]))-bool(sum([pressed[x] for x in self.right])),
		        bool(sum([pressed[x] for x in self.up]))-bool(sum([pressed[x] for x in self.down]))][axis]
	def get_button(self, button):
		pressed = pygame.key.get_pressed()
		if button==0: return bool(sum([pressed[x] for x in self.jump]))
	def update(self):
		pressed = pygame.key.get_pressed()
		self.buttonstatus = [bool(sum([pressed[x] for x in y])) for y in (self.jump, self.heavyatk, self.lightatk, self.dodge)]
		if self.oldbuttonstatus != self.buttonstatus:
			for x in range(len(self.buttonstatus)):
				if self.buttonstatus[x]==1 and self.oldbuttonstatus[x]==0: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN, {"button":x}))
			self.oldbuttonstatus = self.buttonstatus[:]
