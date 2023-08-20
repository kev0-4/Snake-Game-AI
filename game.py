import pygame
import random
import numpy as np
from collections import namedtuple
from enum import Enum

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# colors
WHITE = (238, 238, 238)
RED = (255, 0, 117) 
GREEN1 = (0, 255, 202)
GREEN2 = (119, 217, 112)
BLACK = (39, 55, 77)  

BLOCK_SIZE = 20
SPEED = 40


class SnakeAI:
    def __init__(self, w=640, h=480) -> None:
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._Place_food()
        self.frame_iteration = 0

    def _Place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._Place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1.user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2.Move
        self._move(action)
        self.snake.insert(0, self.head)

        # 3.Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4.Place new food or move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._Place_food()
        else:
            self.snake.pop()

        # 5 update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits body
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: "+str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN,
                      Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4  # for if we are on last idx
            new_dir = clock_wise[next_idx]
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4  # for if first index
            new_dir = clock_wise[next_idx]

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
