import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent: #defines a class for the agent

    def __init__(self): #defines a function for initializing the agent
        self.n_games = 0 #number of games played
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen = MAX_MEMORY) #popleft()
        self.model = Linear_QNet(11, 256, 3) #input size, hidden size, output size
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma) 
        #model, trainer

    def get_state(self, game): #defines a function that takes the parameters of self and game
        head = game.snake[0] #gets the head of the snake
        point_l = Point(head.x - 20, head.y) #creates a point to the left of the head
        point_r = Point(head.x + 20, head.y) #creates a point to the right of the head
        point_u = Point(head.x, head.y - 20) #creates a point above the head
        point_d = Point(head.x, head.y + 20) #creates a point below the head

        dir_l = game.direction == Direction.LEFT #checks if the snake is moving left
        dir_r = game.direction == Direction.RIGHT #checks if the snake is moving right
        dir_u = game.direction == Direction.UP #checks if the snake is moving up
        dir_d = game.direction == Direction.DOWN #checks if the snake is moving down

        state = [
            #danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            #danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            #Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            #Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #Food location
            game.food.x < game.head.x, #food left
            game.food.x > game.head.x, #food right
            game.food.y < game.head.y, #food up
            game.food.y > game.head.y  #food down
            ]
        
        return np.array(state, dtype = int) #returns the state as a numpy array of integers

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #popleft if MAX_MEMORY is reached

    def train_long_memory(self): #defines a function for training long-term memory
        if len(self.memory) > BATCH_SIZE: #checks if the length of memory is greater than the batch size
            mini_sample = random.sample(self.memory, BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory #list of tuples
        
        states, actions, rewards, next_states, dones = zip(*mini_sample) #unzips the mini_sample into separate lists
        self.trainer.train_step(states, actions, rewards, next_states, dones) #trains the model with the mini_sample
        #for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done): #defines a function for training short-term memory
        self.trainer.train_step(state, action, reward, next_state, done) #trains the model with the given parameters

    def get_action(self, state):
        #random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games #decrease epsilon as number of games increases
        final_move = [0, 0, 0] #initializes the final move as a list of three zeros
        if random.randint(0, 200) < self.epsilon: #random move
            move = random.randint(0, 2) #chooses a random move between 0 and 2
            final_move[move] = 1 #sets the chosen move to 1
        else:
            state0 = torch.tensor(state, dtype = torch.float) #converts the state to a tensor
            prediction = self.model(state0) #predicts the action values using the model
            move = torch.argmax(prediction).item() #chooses the move with the highest predicted value
            final_move[move] = 1 #sets the chosen move to 1

        return final_move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember 
        agent.remember(state_old, final_move, reward, state_new, done)

        if done: #if the game is done
            #train long memory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game:', agent.n_games, 'Score:', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__': #if this file is being run directly
    train()