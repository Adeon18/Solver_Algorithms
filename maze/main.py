'''
main module for the chess
pygame interface is located here
'''
import pygame
import sys
from os import path

import time
from maze import *
from pygame_helpers import *


class Game:
    DARKPINK = (219, 0, 189)
    DARKBLUE = (95, 0, 219)
    LIGHTBLUE = (138, 138, 219)
    LIGHTPINK = (192, 138, 219)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        # Make screen
        self.screen = pygame.display.set_mode((800, 800))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scr_width, self.scr_height = pygame.display.get_surface().get_size()
        pygame.display.set_caption("Maze Solver")
        # Load data and start te clock
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        """
        Load all the external data
        """
        game_folder = path.dirname(__file__)

    def new(self):
        """
        New game
        """
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.maze_obj = Maze('maze_file.txt', visualization=self)
        self.TIMESTEP = 50
        self.create_maze()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(60) / 1000.0
            self.events()
            self.draw()
            self.update()
    
    def create_maze(self):
        """
        Just draw the maze begginning and then just update the tiles
        """
        for i in range(0, len(self.maze_obj.maze)):
            for j in range(0, len(self.maze_obj.maze[i])):
                Tile(self, self.maze_obj, j, i)

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        """
        The whole game process logic that need to be updated each second
        """
        pygame.time.wait(2000)
        self.maze_obj.find_path()
        pygame.time.wait(5000)
        self.quit()

    def draw(self):
        """
        Blit everything to the screen each frame
        """
        self.screen.fill((125, 100, 158))
        self.draw_text(f"Delay: {self.TIMESTEP} ms", 40, (51, 16, 97), self.scr_width//2, 50)
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    self.quit()
                if event.key == pygame.K_UP:
                    self.TIMESTEP -= 10
                if event.key == pygame.K_DOWN:
                    self.TIMESTEP += 10

    def wait_for_key(self):
        """
        Wait for ANY key pressed by the user
        """
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y, align='center', fontname="Consolas"):
        """
        Helper for drawing text on the screen
        """
        font = pygame.font.SysFont(path.join("Consolas", fontname), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)



if __name__ == "__main__":
    # create the game object
    g = Game()
    while True:
        g.new()
        g.run()