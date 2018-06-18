import pygame

class dummyJoystick(): #fake joystick class, emulates pygame joytick object using keyboard
	def __init__(self, joy, left=[pygame.K_a], right=[pygame.K_d], down=[pygame.K_s], up=[pygame.K_w],\
	jump=[pygame.K_SPACE], heavyatk=[pygame.K_j], lightatk=[pygame.K_k], dodge=[pygame.K_l]):
		self.joy = joy #stores joystick id
		self.left = left #stores keyboard buttons for joystick buttons (some unused)
		self.right = right
		self.down = down
		self.up = up
		self.jump = jump
		self.heavyatk = heavyatk
		self.lightatk = lightatk
		self.dodge = dodge
	def get_axis(self, axis): #emulate joystick position with keys
		pressed = pygame.key.get_pressed()
		return -[bool(sum([pressed[x] for x in self.left]))-bool(sum([pressed[x] for x in self.right])),
		        bool(sum([pressed[x] for x in self.up]))-bool(sum([pressed[x] for x in self.down]))][axis]
	def get_button(self, button): #return whether keyboard button is pressed
		pressed = pygame.key.get_pressed()
		if button==0: return bool(sum([pressed[x] for x in self.jump]))
		if button==1: return bool(sum([pressed[x] for x in self.heavyatk]))
		if button==2: return bool(sum([pressed[x] for x in self.lightatk]))
		if button in(4,5): return bool(sum([pressed[x] for x in self.dodge]))
	def get_id(self): return self.joy #returns joystick ID
	def update(self, events): #must be called every frame, generates joystick button presses from keyboard events
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key in self.jump: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":0}))
				if e.key in self.heavyatk: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":2}))
				if e.key in self.lightatk: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":1}))
				if e.key in self.dodge: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":4}))
			if e.type == pygame.KEYUP:
				if e.key in self.jump: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONUP,{"joy":self.joy,"button":0}))
				if e.key in self.heavyatk: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONUP,{"joy":self.joy,"button":2}))
				if e.key in self.lightatk: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONUP,{"joy":self.joy,"button":1}))
				if e.key in self.dodge: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONUP,{"joy":self.joy,"button":4}))
	def get_name(self): return "Dummy Joystick" #returns joystick name
