class grid(): #grid data structure
	def __init__(self, width, height):		self._2dlist = [[None for y in range(width)] for x in range(height)]
	def __getitem__(self, pos):			return self._2dlist[pos[1]][pos[0]]
	def __setitem__(self, pos, val):		self._2dlist[pos[1]][pos[0]]=val
	def __repr__(self):				return "\n".join([" ".join([str(x) for x in y]) for y in self._2dlist][::-1])
	def __len__(self):				return len(self._2dlist)*len(self._2dlist[0])
	def get_width(self):				return len(self._2dlist[0])
	def get_height(self):				return len(self._2dlist)

class button_grid(grid): #drawable grid datatype
	def __init__(self, width, height, rect):
		self._rect=rect;
		self._2dlist = [[button((y*rect[2]/width+rect[0]+1,x*rect[3]/height+rect[1]+1,rect[2]/width-2,rect[3]/height-2)) for y in range(width)] for x in range(height)]
		self._surface = pygame.Surface((self._rect[2], self._rect[3]))
		self._surface.fill((255,255,255))
	def get_rect(self):				return self._rect
	def draw(self): #make a list of surfaces then blit them to the main surface
		blitlist = []
		for y in range(len(self._2dlist)):
			for x in range(len(self._2dlist[y])):
				try:blitlist.append((self._2dlist[y][x].draw(),x,y))
				except:() #ignore if error in / no .draw() method, abused for optimisation
		for x in blitlist: self._surface.blit(x[0],(x[1]*(self._rect[2]/self.get_width()),x[2]*(self._rect[3]/self.get_height()))) #blit everything in its place
		return self._surface
	def update(self): return[[x.update()for x in y]for y in self._2dlist] #call update method on all contained objects, return array of results

class letter_grid(button_grid): #generate drawable grid from letter input
	def __init__(self, letters, rect):
		button_grid.__init__(self, len(letters[0]), len(letters), rect)
		for y in range(len(letters)):
			for x in range(len(letters[y])):self[x,y].set_text(letters[y][x])

class menu(letter_grid):
	def __init__(self, items, rect):
		letter_grid.__init__(self, [[x] for x in items], rect) #calculate font size from max width of words
		calc = pygame.font.SysFont(pygame.font.match_font("lucida","mono","couriernew"), 10).render("e",1,(0,0,0)).get_width()/10
		for y in range(len(items)):self[0,y].set_font(pygame.font.SysFont(pygame.font.match_font("lucida","mono","couriernew"),int((self._rect[2]/(max([len(x) for x in items])+2))/calc)))
	def update(self):
		states=[x[0].update()for x in self._2dlist] #call update method on all contained objects, return clicked item
		try:return states.index(1)
		except:return None

class button():
	def __init__(self, rect, text="", bgcolour=(255,255,255), bordercolour=(0,0,0), textcolour=(0,0,0), hovercolour=(128,128,128), activecolour=(0,128,0), lockcolour=(128,0,128), function=None):
		self._rect =		rect #store variables in self
		self._text =		text
		self._bgcolour =	bgcolour
		self._bordercolour =	bordercolour
		self._textcolour =	textcolour
		self._hovercolour =	hovercolour
		self._activecolour =	activecolour
		self._lockcolour =	lockcolour
		self._function =	function
		self._state =		0
		self._previous =	-1
		self._surface =		pygame.Surface((rect[2], rect[3]))
		#calculate fontsize
		calc = pygame.font.SysFont(pygame.font.match_font("lucida","mono","couriernew"), 10).render("e",1,(0,0,0)).get_width()/10
		self._font=pygame.font.SysFont(pygame.font.match_font("lucida","mono","couriernew"), int((rect[2]/(len(text)+2))/calc))
	def __repr__(self):				return self._text
	def set_font(self, font): self._font=font #used to override font size
	def set_text(self, text): #recalculate font size and change text
		self._text = text
		calc = pygame.font.SysFont(pygame.font.match_font("lucida","mono","couriernew"), 10).render("e",1,(0,0,0)).get_width()/10
		self._font=pygame.font.SysFont(pygame.font.match_font("lucida","mono","couriernew"), int((self._rect[2]/(len(text)+2))/calc))
	def set_colours(self, bg=None, border=None, text=None, hover=None, active=None, lock=None): #change colours
		if bg:		self._bgcolour=bg
		if border:	self._bordercolour=border
		if text:	self._textcolour=text
		if hover:	self._hovercolour=hover
		if active:	self._activecolour=active
		if lock:	self._lockcolour=lock
	def set_state(self, state): self._state=state #run this only after updates to force a button state
	def get_state(self): return self._state
	def draw(self):
		0/(self._previous!=self._state) #""optimisation"", forces the button_grid class to skip drawing the button
		exec({ #change fill colour based on state
			0:"self._surface.fill(self._bgcolour)",
			1:"self._surface.fill(self._hovercolour)",
			2:"self._surface.fill(self._activecolour)",
			3:"self._surface.fill(self._lockcolour)",
			4:"self._surface.fill(self._hovercolour)"
		}[self._state]) #hacky way of doing switch statements in python, because nobody wants 3 elifs
		pygame.draw.rect(self._surface, self._bordercolour, (0,0,self._rect[2],self._rect[3]), 1) #draw border
		render = self._font.render(self._text, 1, self._textcolour) #draw text
		self._surface.blit(render, (self._rect[2]/2-render.get_width()/2, self._rect[3]/2-render.get_height()/2))
		return self._surface
	def update(self):
		self._previous = self._state
		if pygame.Rect(self._rect).collidepoint(pygame.mouse.get_pos()): self._state=1
		else: self._state=0
		if self._state and pygame.mouse.get_pressed()[0]: self._state=2
		if self._state and pygame.mouse.get_pressed()[2]: self._state=4
		if self._state!=2 and self._previous==2: return 1
		if self._state!=4 and self._previous==4: return 2
		return 0
