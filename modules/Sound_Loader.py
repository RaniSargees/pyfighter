#Sound_loader
#Loads in sounds and plays them on command
import pygame, os, sys

class Sound_Manager():
	def __init__(self):
		game_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
		self.sfx_folder = os.path.join(game_folder, 'SFX')#Loads in Sound folder
		self.sfx_list = {}
		for fileName in os.listdir(self.sfx_folder): #Load Sound Effects from SFX folder
			file = os.path.join(self.sfx_folder,fileName)
			self.sfx_list[str(fileName[:-4])] = file
	def load(self,name): #load sound from sfx list
		return pygame.mixer.Sound(self.sfx_list[name])

	def play(self,name,loops = 0, maxtime = 0, fade_ms = 0): #play sound from sfx list
		temp = pygame.mixer.Sound(self.sfx_list[name])
		temp.play(loops,maxtime,fade_ms)

	def stop_all(self): #stops all sounds
		pygame.mixer.stop()
		pygame.mixer.music.stop()

	def load_music(self,name): #load music from sfx list
		pygame.mixer.music.load(self.sfx_list[name])
