import torch
import random
import numpy as np
from game import SnakeAI, Direction, Point
from collections import deque  # ds to store memory
from model import Linear_QNet, QTrainer
from plotting import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000 # 500
LR = 0.001  # learning rate


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness control
        self.gamma = 0.98 #0.8  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        # (input size, hidden size(changable), output size)
        self.model = Linear_QNet(11, 256, 3) 
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_states(self, game):
        head = game.snake[0]  # gets head of snake
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger Straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.food.y  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        # popleft if max memory is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(
                self.memory, BATCH_SIZE)  # list of tuples
        else:  # If less than Batch_sieze we take whole memory
            mini_sample = self.memory
        states, actions, rewards, next_states, done = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, done)

    def train_short_memory(self,  state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

# gpt edits
    def get_action(self, state):
        # random moves exploration and gradually decrease randomness
        self.epsilon = 80 - self.n_games
        num_moves = 3  # Number of possible moves
        final_move = [0] * num_moves  # Initialize with zeros
        if random.randint(0, 200) < self.epsilon:
            # Adjust for zero-based indexing
            move = random.randint(0, num_moves - 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # Ensure move is within the valid range
            move = torch.argmax(prediction).item()
            if move < 0:
                move = 0
            elif move >= num_moves:
                move = num_moves - 1
            final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeAI()
    epoch = 0
    max_epochs = 600 # Number of Episodes (500 - 1000 for optimal score)
    while epoch < max_epochs:
        # get old state
        state_old = agent.get_states(game)

        # get move based on current state
        final_move = agent.get_action(state_old)

        # perform and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_states(game)

        # train short memory (for 1 step)
        agent.train_short_memory(
            state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory (experience replay), ploat results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

            epoch += 1
    print("Training completed after", max_epochs,"epochs.")


if __name__ == '__main__':
    train()
