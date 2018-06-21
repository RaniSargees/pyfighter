import pygame

class joystick_bot():#Bot controlled joystick
	def __init__(self,joy):
		self.joy = joy
		self.pressed = [0,0,0,0,0,0,0]
		self.timer = 0
		#0 - Left
		#1 - Right
		#2 - Up
		#3 - Down
		#4 - Jump
		#5 - Heavy
		#6 - Light
	def get_axis(self,axis): return -[(self.pressed[0])-(self.pressed[1]), (self.pressed[2])-(self.pressed[3])][axis]
	def get_id(self): return self.joy
	def get_name(self): return "Joystick AI"
	def get_button(self, button): return self.pressed[4+button]
	def update(self, events, data=[],player=None):#Run bot events here
		self.timer += 1
		data.pop(data.index(player))
		self.pressed = [0 for x in self.pressed]
		if player.x > data[0].x and player.x > 200:
			self.pressed[0] = 1
		elif player.x < data[0].x and player.x < 1080:
			self.pressed[1] = 1
		else:
			self.pressed[0],self.pressed[1] = 0,0
		
		if abs(player.x - data[0].x) < 50 and not(self.timer%30):
			self.pressed[6] = 1
		
		if abs(player.x - data[0].x) > 200 and not(self.timer%10):
			self.pressed[5] = 1
		
		if player.y > 500 and not(player.grounded):
			self.pressed[2] = 1
			self.pressed[5] = 1
			
		if (player.y > data[0].y+10) and self.timer%30:
			self.pressed[4] = 1
		elif (player.y < data[0].y) and player.grounded:
			self.pressed[3] = 1
			
		
		self.updateEvents()
	
	
	def updateEvents(self):
		if self.pressed[4]: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":0}))
		if self.pressed[5]: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":1}))
		if self.pressed[6]: pygame.event.post(pygame.event.Event(pygame.JOYBUTTONDOWN,{"joy":self.joy,"button":2}))
		
		