import pygame, sys, random, time

class Snake:
    def __init__(self, width=50, height=50, thickness=10):
        self.possible_actions = ['RIGHT', 'LEFT', 'UP', 'DOWN']
        self.game_over = False
        self.width = width
        self.height = height
        self.thickness = thickness
        # whether it should render anything
        self.display=display
        # Important varibles
        self.snakePos = [100, 50]
        self.snakeBody = [[100,50], [90,50], [80,50]]
        self.foodPos = [random.randrange(1,width)*self.thickness, random.randrange(1,height)*self.thickness]
        self.foodSpawn = True

        self.direction = 'RIGHT'
        self.changeto = self.direction

        # Colors
        self.red = pygame.Color(255, 0, 0) # gameover
        self.green = pygame.Color(0, 255, 0) #snake
        self.black = pygame.Color(0, 0, 0) #score
        self.white = pygame.Color(255, 255, 255) #background
        self.brown = pygame.Color(165, 42, 42) #food

        self.score = 0
            
    def init_interface(self):
        self.pygame = pygame
        check_errors = self.pygame.init()
        if check_errors[1] > 0:
            print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
            sys.exit(-1)
        else:
            print("(+) PyGame successfully initialized!")
        self.fpsController = self.pygame.time.Clock()
        # Play surface
        self.playSurface = self.pygame.display.set_mode((self.height*self.thickness, self.width*self.thickness))
        self.pygame.display.set_caption('Snake game!')
    
    def get_states(self):
        ''' Gets the relevant states of the game used in the AI
        '''
        return { 
            'score': self.score,
            'snake_pos': {
                'x': self.snakePos[1],
                'y': self.snakePos[0]
            },
            'food_pos': {
                'x': self.foodPos[1],
                'y': self.foodPos[0]
            },
            'snake_body': self.snakeBody,
            'is_game_over': self.game_over,
            'border_distances': {
                'right':0,
                'left':self.snakePos[1],
                'up':0,
                'down':self.snakePos[0]
            }
        }
    
    def render_game_over(self):
        if self.game_over:
            myFont = self.pygame.font.SysFont('monaco', self.height)
            GOsurf = myFont.render('Game over!', True, self.red)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = ((self.thickness*self.width/2), 1.5*self.thickness)
            self.playSurface.blit(GOsurf,GOrect)
            self.render_score(0)
            self.pygame.display.flip()
            time.sleep(4)
            self.pygame.quit() #pygame exit
#             sys.exit() #console exit
    
    def render_score(self,choice=1):
        sFont = self.pygame.font.SysFont('monaco', 24)
        Ssurf = sFont.render('Score : {0}'.format(self.score) , True, self.black)
        Srect = Ssurf.get_rect()
        if choice == 1:
            Srect.midtop = (8*self.thickness, self.thickness)
        else:
            Srect.midtop = (self.thickness*(self.width/2), 12*self.thickness)
        self.playSurface.blit(Ssurf,Srect)
    
    def get_pressed_key(self):
        ''' Gets the key that was pressed by the user
        '''
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.game_over = True
            elif event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_RIGHT or event.key == ord('d'):
                    self.changeto = 'RIGHT' 
                if event.key == self.pygame.K_LEFT or event.key == ord('a'):
                    self.changeto = 'LEFT' 
                if event.key == self.pygame.K_UP or event.key == ord('w'):
                    self.changeto = 'UP' 
                if event.key == self.pygame.K_DOWN or event.key == ord('s'):
                    self.changeto = 'DOWN' 
                if event.key == self.pygame.K_ESCAPE:
                    self.pygame.event.post(self.pygame.event.Event(self.pygame.QUIT))
                    
    def set_changed_to(action):
        self.changeto = action
    
    def move_snake(self):
        ''' Move the snake
        '''
        # validation of self.direction
        if self.changeto == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if self.changeto == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if self.changeto == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if self.changeto == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

        # Update snake position [x,y]
        if self.direction == 'RIGHT':
            self.snakePos[0] += self.thickness
        if self.direction == 'LEFT':
            self.snakePos[0] -= self.thickness
        if self.direction == 'UP':
            self.snakePos[1] -= self.thickness
        if self.direction == 'DOWN':
            self.snakePos[1] += self.thickness
            
        # Snake body mechanism
        self.snakeBody.insert(0, list(self.snakePos))
        if self.snakePos[0] == self.foodPos[0] and self.snakePos[1] == self.foodPos[1]:
            self.score += 1
            self.foodSpawn = False
        else:
            self.snakeBody.pop()

    def spawn_food(self):
        #Food Spawn
        if self.foodSpawn == False:
            self.foodPos = [random.randrange(1,self.width)*self.thickness,random.randrange(1, self.height)*self.thickness] 
        self.foodSpawn = True

    def check_game_over(self):
        # Bound
        if self.snakePos[0] > (self.height-1)*self.thickness or self.snakePos[0] < 0:
            self.game_over = True
        if self.snakePos[1] > (self.width-1)*self.thickness or self.snakePos[1] < 0:
            self.game_over = True
        # Self hit
        for block in self.snakeBody[1:]:
            if self.snakePos[0] == block[0] and self.snakePos[1] == block[1]:
                self.game_over = True
    
    def render(self):
        #Background
        self.playSurface.fill(self.white)
        #Draw Snake 
        for pos in self.snakeBody:
            self.pygame.draw.rect(self.playSurface, self.green, self.pygame.Rect(pos[0],pos[1],self.thickness,self.thickness))

        self.pygame.draw.rect(self.playSurface, self.brown, self.pygame.Rect(self.foodPos[0], self.foodPos[1],self.thickness,self.thickness))
        self.render_score()
        self.pygame.display.flip()
        self.fpsController.tick(24)
    
    def play_game(self):
        self.init_interface()
        while self.game_over == False:
            self.get_pressed_key()
            self.move_snake()
            self.spawn_food()
            self.render()
            self.check_game_over()
        self.render_game_over()
