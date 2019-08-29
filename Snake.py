import pygame, sys, random, time
import gym
from gym import spaces
import numpy as np

class Snake(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, width=50, thickness=10):
        super(Snake, self).__init__()
        # make it square for the sake of defining the state space
        self.height=width
        self.possible_actions = ['RIGHT', 'LEFT', 'UP', 'DOWN']
        # Define action and observation spaces following openai standard
        self.action_space = spaces.Discrete(len(self.possible_actions))
        self.observation_space = spaces.Box(-1, width+1, (8,1), dtype=np.float32)
        # Define other internal variables
        self.width = width
        self.thickness = thickness
        # whether it should render anything
        self.display=display
        # Important varibles
        self.reset()

        # Colors
        self.red = pygame.Color(255, 0, 0) # gameover
        self.green = pygame.Color(0, 255, 0) #snake
        self.black = pygame.Color(0, 0, 0) #score
        self.white = pygame.Color(255, 255, 255) #background
        self.brown = pygame.Color(165, 42, 42) #food
            
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
    
    def close_render(self):
        self.pygame.quit()
    
    def get_states(self):
        ''' Gets the relevant states of the game used in the AI
        '''
        state_dict = {  
            'snake_pos_x':self.snakePos[1],
            'snake_pos_y':self.snakePos[0],
            'food_pos_x':self.foodPos[1],
            'food_pos_y':self.foodPos[0],
#             'snake_body': self.snakeBody,
            # 'is_game_over': 1 if self.game_over else 0]],
            'border_distances_right':abs((self.width-1) - self.snakePos[0]),
            'border_distances_left':self.snakePos[0],
            'border_distances_up':abs((self.height-1) - self.snakePos[1]),
            'border_distances_down':self.snakePos[1]
        }
        return state_dict
    
    def get_gym_state_representation(self):
        ret_list = []
        dict_states = self.get_states()
        for i in dict_states:
            ret_list.append([dict_states[i]])
        return np.array(ret_list)

    def calculate_immediate_reward(self):
        reward = 0
        if self.is_in_food_position():
            reward = 10
        elif self.game_over:
            reward = -10
        # else:
        #     # reward for the distance to the food
        #     reward = 1/(abs(self.snakePos[0] - self.foodPos[0]) + abs(self.snakePos[1] - self.foodPos[1]))
        return reward
        
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
            self.close_render()
    
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
        change_to = self.direction
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.game_over = True
            elif event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT' 
                if event.key == self.pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT' 
                if event.key == self.pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP' 
                if event.key == self.pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN' 
                if event.key == self.pygame.K_ESCAPE:
                    self.pygame.event.post(self.pygame.event.Event(self.pygame.QUIT))
        return change_to
    
    def move_snake(self, change_to):
        ''' Move the snake
        '''
        self.spawn_food()
        # validation of self.direction
        if change_to == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if change_to == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if change_to == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if change_to == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

        # Update snake position [x,y]
        if self.direction == 'RIGHT':
            self.snakePos[0] += 1 #self.thickness
        if self.direction == 'LEFT':
            self.snakePos[0] -= 1 #self.thickness
        if self.direction == 'UP':
            self.snakePos[1] -= 1 #self.thickness
        if self.direction == 'DOWN':
            self.snakePos[1] += 1 #self.thickness
            
        # Snake body mechanism
        self.snakeBody.insert(0, list(self.snakePos))
        if self.is_in_food_position():
            self.score += 1
            self.foodSpawn = False
            # test not growing snake
#             self.snakeBody.pop()
        else:
            self.snakeBody.pop()
        self.check_game_over()
    
    def is_in_food_position(self):
        return self.snakePos[0] == self.foodPos[0] and self.snakePos[1] == self.foodPos[1]

    def spawn_food(self):
        #Food Spawn
        if self.foodSpawn == False:
            self.foodPos = [random.randrange(1,self.height-1),#*self.thickness,
                            random.randrange(1, self.width-1)#*self.thickness
                           ] 
        self.foodSpawn = True

    def check_game_over(self):
        # Bound
        if self.snakePos[0] > (self.height-1) or self.snakePos[0] < 0:
            self.game_over = True
        if self.snakePos[1] > (self.width-1) or self.snakePos[1] < 0:
            self.game_over = True
        # Self hit
        for block in self.snakeBody[1:]:
            if self.snakePos[0] == block[0] and self.snakePos[1] == block[1]:
                self.game_over = True
    
    def play_game(self):
        self.init_interface()
        while self.game_over == False:
            direction = self.get_pressed_key()
            self.move_snake(direction)
            self.render()
        self.render_game_over()
    
    def step(self, action):
        ''' step method for openai
        returns: observation, reward, done, info 
        '''
        # moves the snake
        self.move_snake(self.possible_actions[action])
        # make the observation
        obs = self.get_gym_state_representation()
        # get the reward 
        rwd = self.calculate_immediate_reward()
        # check if it is done
        done = self.game_over
        # more info
        info = {}
        return obs, rwd, done, info
    
    def reset(self):
        ''' reset method for openai
        '''
        self.snakePos = [10, 5]
        self.snakeBody = [[10,5], [9,5], [8,5]]
        self.foodSpawn = False
        self.spawn_food()
        self.game_over = False
        self.direction = 'RIGHT'
        self.score=0
        return self.get_gym_state_representation()
    
    def render(self, mode='human', close=False):
        ''' Render method for openai
        '''
        self.init_interface()
        #Background
        self.playSurface.fill(self.white)
        #Draw Snake 
        for pos in self.snakeBody:
            self.pygame.draw.rect(self.playSurface, self.green, self.pygame.Rect(self.thickness*pos[0],self.thickness*pos[1],self.thickness,self.thickness))

        self.pygame.draw.rect(self.playSurface, self.brown, self.pygame.Rect(self.thickness*self.foodPos[0], self.thickness*self.foodPos[1],self.thickness,self.thickness))
        self.render_score()
        self.pygame.display.flip()
        self.fpsController.tick(20)
            

        
