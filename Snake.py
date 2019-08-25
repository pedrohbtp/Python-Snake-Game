import pygame, sys, random, time

class Snake:
    def __init__(self):
        # Important varibles
        self.snakePos = [100, 50]
        self.snakeBody = [[100,50], [90,50], [80,50]]
        self.fpsController = pygame.time.Clock()
        self.foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
        self.foodSpawn = True

        self.direction = 'RIGHT'
        self.changeto = self.direction

        self.score = 0
        self.pygame = pygame
        self.check_pygame()
        self.init_surface()
    
    def check_pygame(self):
        check_errors = self.pygame.init()
        if check_errors[1] > 0:
            print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
            sys.exit(-1)
        else:
            print("(+) PyGame successfully initialized!")
            
    def init_surface(self):
        # Play surface
        self.playSurface = self.pygame.display.set_mode((720, 460))
        self.pygame.display.set_caption('Snake game!')

        # Colors
        self.red = self.pygame.Color(255, 0, 0) # gameover
        self.green = self.pygame.Color(0, 255, 0) #snake
        self.black = self.pygame.Color(0, 0, 0) #score
        self.white = self.pygame.Color(255, 255, 255) #background
        self.brown = self.pygame.Color(165, 42, 42) #food
    
    def gameOver(self):
        myFont = self.pygame.font.SysFont('monaco', 72)
        GOsurf = myFont.render('Game over!', True, self.red)
        GOrect = GOsurf.get_rect()
        GOrect.midtop = (360, 15)
        self.playSurface.blit(GOsurf,GOrect)
        self.showScore(0)
        self.pygame.display.flip()

        time.sleep(4)
        self.pygame.quit() #pygame exit
        sys.exit() #console exit
    
    def showScore(self,choice=1):
        sFont = self.pygame.font.SysFont('monaco', 24)
        Ssurf = sFont.render('Score : {0}'.format(self.score) , True, self.black)
        Srect = Ssurf.get_rect()
        if choice == 1:
            Srect.midtop = (80, 10)
        else:
            Srect.midtop = (360, 120)
        self.playSurface.blit(Ssurf,Srect)
    
    def move_snake(self):
        ''' Move the snake
        '''
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.pygame.quit()
                sys.exit()
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
            self.snakePos[0] += 10
        if self.direction == 'LEFT':
            self.snakePos[0] -= 10
        if self.direction == 'UP':
            self.snakePos[1] -= 10
        if self.direction == 'DOWN':
            self.snakePos[1] += 10
            
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
            self.foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10] 
        self.foodSpawn = True

    def check_game_over(self):
        # Bound
        if self.snakePos[0] > 710 or self.snakePos[0] < 0:
            self.gameOver()
        if self.snakePos[1] > 450 or self.snakePos[1] < 0:
            self.gameOver()
        # Self hit
        for block in self.snakeBody[1:]:
            if self.snakePos[0] == block[0] and self.snakePos[1] == block[1]:
                self.gameOver()

    def draw_snake(self):
        #Draw Snake 
        for pos in self.snakeBody:
            self.pygame.draw.rect(self.playSurface, self.green, self.pygame.Rect(pos[0],pos[1],10,10))

        self.pygame.draw.rect(self.playSurface, self.brown, self.pygame.Rect(self.foodPos[0], self.foodPos[1],10,10))

    def draw_background(self):
        #Background
        self.playSurface.fill(self.white)
    
    def main_loop(self):
        while True:
            self.move_snake()
            self.spawn_food()
            self.draw_background()
            self.draw_snake()
            self.check_game_over()
            
            self.showScore()
            
            self.pygame.display.flip()

            self.fpsController.tick(24)
