import pygame
import sys
from os import path

import time
from maze import *


class Tile(pygame.sprite.Sprite):
    TILESIZE = 0
    def __init__(self, game, maze, grid_x, grid_y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.maze = maze
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.TILEWIDTH = 600 // len(self.maze.maze)
        self.TILEHEIGHT = 600 // len(self.maze.maze[0])
        self.image = pygame.Surface((self.TILEWIDTH, self.TILEWIDTH))
        # Color the images
        if self.maze.maze[self.grid_y][self.grid_x] == self.maze.MAZE_WALL:
            self.image.fill(self.game.BLACK)
        elif self.maze.maze[self.grid_y][self.grid_x] == self.maze.EXIT:
            self.image.fill(self.game.DARKBLUE)
        elif self.maze.maze[self.grid_y][self.grid_x] == -1:
            self.image.fill(self.game.DARKPINK)
        else:
            self.image.fill(self.game.WHITE)
        self.rect = self.image.get_rect()

        self.piece = None
        self.selected = False

        self.rect.x = 100 + (self.grid_x) * self.TILEWIDTH
        self.rect.y = 100 + (self.grid_y) * self.TILEWIDTH
    
    def update(self):
        """
        Update the sprites view
        """
        # Fill each tile the needed color
        if self.maze.maze[self.grid_y][self.grid_x] == self.maze.MAZE_WALL:
            self.image.fill(self.game.BLACK)
        elif self.maze.maze[self.grid_y][self.grid_x] == self.maze.EXIT:
            self.image.fill(self.game.DARKPINK)
        elif self.maze.maze[self.grid_y][self.grid_x] == -1:
            self.image.fill(self.game.DARKBLUE)
        elif self.maze.maze[self.grid_y][self.grid_x] == self.maze.PATH_TOKEN:
            self.image.fill(self.game.LIGHTPINK)
        elif self.maze.maze[self.grid_y][self.grid_x] == self.maze.TRIED_TOKEN:
            self.image.fill(self.game.LIGHTBLUE)
        else:
            self.image.fill(self.game.WHITE)