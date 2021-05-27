"""
This module contains pygame helpers for visualization
"""
import pygame

from maze import *


class Tile(pygame.sprite.Sprite):
    """
    A tile object that gets colored during the process
    """
    TILESIZE = 0
    def __init__(self, game, maze, grid_x, grid_y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Some constants
        self.game = game
        self.maze = maze
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.TILEWIDTH = 600 // len(self.maze.maze)
        self.TILEHEIGHT = 600 // len(self.maze.maze[0])
        # Get the "image"
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
        # Get the rect
        self.rect = self.image.get_rect()
        # Position it
        self.rect.x = 100 + (self.grid_x) * self.TILEWIDTH
        self.rect.y = 100 + (self.grid_y) * self.TILEWIDTH
    
    def update(self):
        """
        Update the tile view in realtime
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