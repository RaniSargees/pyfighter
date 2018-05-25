##################BUTTON CLASS###################
#              By: Ryota Parsons                # 
#                                               # 
#Functions: Creates a dynamic button with       #
#   different attributes depending on what      #
#   is passed.                                  # 
#                                               # 
#Inputs: Surface -> Surface to blit button on   #
#        Color -> Color of the button           #
#        Text -> Text displayed on Button       # 
#        Location -> X and Y cords of Button    #
#        Size -> Width and Height of Button     #
#        MouseColor -> Color of Button when     #
#   mouse is hovering over it                   # 
#        tColor -> Color of the text            #  
#        setting -> See definition under init   #
#        Fn -> Function ran when btn is clicked #
#        Font -> Font size of the button        #     
#        MaxFont -> Uses max font size in X dir # 
#        State2 -> Color of BTN when state = 2  # 
#################################################
import pygame
try:
    import settings
except:
    print('Setting folder not found. No global variables are being imported')
class BTN(pygame.sprite.Sprite):
    def __init__(self,surface,color,text,location,size,MouseColor = None,tcolor = None,setting = 0,Fn = None, Font = None, MaxFont = False, State2 = (0,255,0)):

        #Settings: 0 = Button (Has blue outline when mouse over, Highlighted MouseColor when clicked)
        #          1 = Button (Has MouseColor highlight when mouse over)  
        #          2 = Word Only. (Cross out when force of 2 is passed)
        #
        #Note: For all BTN instances if a command is passed to the paramter Fn it will be executed on Button press
        #      When passing values to Fn. They must be as a string. (Exec is used to run it)
        self.rect = pygame.Rect(location, size)
        self.surface = surface
        self.color = color
        if MouseColor == None:
            self.MouseColor = color
        else:
            self.MouseColor = MouseColor
        self.colorNow = color
        self.loc = location
        self.size = size
        if tcolor == None:
            #By default make the text color be complementary to the button color
            self.tcolor = (255-color[0],255-color[1],255-color[2])
        else:
            self.tcolor = tcolor
        self.set = setting
        #Determine and set Font size
        if MaxFont == True:
            self.charSize = int((size[0]/len(text))*1.58)
        elif Font == None:
            self.charSize = int((size[0]/len(text)))
        else:
            self.charSize = Font
        self.font = pygame.font.SysFont('Courier New',self.charSize)
        self.word = text
        self.text = self.font.render(text,True,self.tcolor)
        self.text_rect = self.text.get_rect(center=(self.loc[0]+(self.size[0]/2),self.loc[1]+(self.size[1]/2)))
        self.Fn = Fn
        self.state = 0
        self.State2 = State2
        self.mLock = True
    def __str__(self):
        return ("This class is a Button class with Settings", self.set,"on state",self.state,"displaying a value of",self.word)
    def update(self,force = 0):
        #force values: 0, Does Nothing (Leave it blank if you want this to happen)
        #              1, Resets all unlocked words (to previous state)
        #              2, Locks highlight. (Color is defualt to green)
	#              3, Tells button that left mouse is clicked
	#              4, Tells button that right mouse is clicked
        mClick = False
        rClick = False
        if force == 1:
            self.state -= 1
            self.mLock = True
        elif force == 2:
            self.state = 2
            self.mLock = True
        elif force == 3:
            mClick = True
            rClick = False
        elif force == 4:
            rClick = True
            mClick = False
        else:
            mClick = False
            rClick = False
            self.mLock = False
        #Do different actions depending on the button state and settings.
        if self.set == 2:
            self.surface.blit(self.text,self.text_rect)
        elif self.set == 1:
            pygame.draw.rect(self.surface,self.colorNow,self.rect)
            pygame.draw.rect(self.surface,(0,0,255),self.rect,3)
            self.surface.blit(self.text,self.text_rect)
        else:
            pygame.draw.rect(self.surface,self.colorNow,self.rect)
            pygame.draw.rect(self.surface,(20,20,20),self.rect,1)
            self.surface.blit(self.text,self.text_rect)
        #Checks if a mouse is on top of its self
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.set == 0:
                pygame.draw.rect(self.surface,(0,0,255),self.rect,3)
            elif self.set == 1:
                self.colorNow = self.MouseColor
            #Checks if the left mouse is clicked
            if mClick == True and self.mLock == False:
                #Selects (put highlight over) button
                if self.set == 0 and self.state%2 == 0:
                    self.state += 1
                #Run a function is there is any
                if not(self.Fn == None):
                    exec(self.Fn)
                    self.mLock = True
            #Checks if the right mouse is clicked
            elif rClick == True and self.state%2 == 1:
                #Returns button to previous state
                self.state -= 1

				
        else:
        #If there is no mouse over the button, return the button to its original state.
            if self.set == 1:
                self.colorNow = self.color
        if self.state%2 == 1:
            #Set the btn color to MouseColor is the state of the button is odd
            self.colorNow = self.MouseColor
        elif self.state == 2:
            #If the state is 2
            if self.set == 2:
                #Cross out word if its on setting 2
                pygame.draw.line(self.surface,(0,0,0),(self.loc[0],self.loc[1]+(self.size[1]/2)),(self.loc[0]+(self.size[0]),self.loc[1]+(self.size[1]/2)),int(self.charSize*0.1))
            #Set the BTN color to State2 (Default to green)
            self.colorNow = self.State2
        else:
            if self.set == 0:
                self.colorNow = self.color
        return self.state
