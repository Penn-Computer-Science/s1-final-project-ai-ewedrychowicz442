import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25) #sets font type and size

# reset
# reward
# play(action) -> direction
# game_iteration
# is_collision

class Direction(Enum):  #sets a class for the directions
    RIGHT = 1 #sets each direction as a number
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

#rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

#set constants
BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:  #sets another class for the snake game 

    def __init__(self, w = 640, h = 480):  #defines a funtion with the parameters of self, width, and height
        self.w = w #sets width of display as 640
        self.h = h #sets height of display as 480
        # init display
        self.display = pygame.display.set_mode((self.w, self.h)) #creates a display with the width and height of 640 and 480
        pygame.display.set_caption('Snake') #creates a title for the display
        self.clock = pygame.time.Clock() #sets the clock
        self.reset() #calls the reset function


    def reset(self): #defines a function that takes the parameter of self
        #init game state
        self.direction = Direction.RIGHT #sets the snake to be facing right when the game is reset

        self.head = Point(self.w/2, self.h/2) #sets the snake head to be in the center of the display
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y), #sets the first block of the snake body to be 20 pixels to the left of the head
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)] #sets the second block of the snake body to be 40 pixels to the left of the head

        self.score = 0 #sets the score as 0
        self.food = None #sets the food as none
        self._place_food() #calls the _place_food function
        self.frame_iteration = 0 #sets the frame iteration as 0 

    def _place_food(self): #defines a function that takes the parameter of self
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE #sets the x value of the food as a random integer between 0 and 620, rounded to the nearest 20 pixels
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE #sets the y value of the food as a random integer between 0 and 460, rounded to the nearest 20 pixels
        self.food = Point(x, y) #sets the food to be at the random point with the random x and y values
        if self.food in self.snake: #checks if the food is on top of the snake
            self._place_food() #calls the _place_food function again if the food is on top of the snake

    def play_step(self, action): #defines a function that takes the parameter of self and action
        self.frame_iteration += 1 
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #2. move
        self._move(action) #update the head
        self.snake.insert(0, self.head)

        #3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        #4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        #5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        #6. return game over and score
        #game_over = False
        return reward, game_over, self.score
    
    def is_collision(self, pt = None):
        if pt is None:
            pt = self.head
        #hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        #hits itself
        if pt in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] #right turn r -> d -> l -> u
        else: #[0, 0, 1]
            next_idx = (idx -1) % 4
            new_dir = clock_wise[next_idx] #left turn r -> u -> l -> d
            
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
