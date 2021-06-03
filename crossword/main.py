'''
Main script with visualization
'''
import pygame
import sys
from os import path, pardir
import random

import time
from crossword import *
# from pygame_helpers import *


class Visualization:
    """
    A general visualization class for pygame
    """
    DARKPINK = (219, 0, 189)
    DARKBLUE = (33, 0, 99)
    LIGHTBLUE = (138, 138, 219)
    LIGHTPINK = (192, 138, 219)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHTRED = (245, 104, 69)
    LIGHTPURPLE = (176, 80, 217)
    LIGHTYELLOW = (250, 232, 95)
    LIGHTGREEN = (116, 250, 95)
    COLORS = [LIGHTBLUE, LIGHTPINK, LIGHTRED, LIGHTPURPLE, LIGHTYELLOW, LIGHTGREEN]
    LETTERSIZE = 67

    def __init__(self):
        """
        Initialize pygame
        """
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        # Make screen
        self.screen = pygame.display.set_mode((800, 800))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scr_width, self.scr_height = pygame.display.get_surface().get_size()
        pygame.display.set_caption("Crossword Solver")
        # Load data and start te clock
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        """
        Load all the external data
        """
        game_folder = path.dirname(path.join(__file__, pardir))
        data_folder = path.join(game_folder, 'data')

    def new(self):
        """
        New visual(Everything is initialized here)
        """
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.crossword = Crossword("../data/crossword.txt", self)
        self.TIMESTEP = 50


    def run(self):
        """
        Run the graphics
        """
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(60) / 1000.0
            self.events()
            self.draw()
            self.update()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        """
        The whole visualization
        """
        pygame.time.wait(2000)
        self.crossword.solve()
        self.draw_text("Solved! Press any key to close.", 40, (51, 16, 97), self.scr_width//2, 750)
        pygame.display.flip()
        self.wait_for_key()
        self.quit()

    def draw(self, color=None):
        """
        Blit everything to the screen each frame
        """
        self.screen.fill((125, 100, 158))
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        
        self.draw_text(f"Delay: {self.TIMESTEP} ms", 40, (51, 16, 97), self.scr_width//2, 50)

        for i in range(len(self.crossword.field)):
            for j in range(len(self.crossword.field[i])):
                if self.crossword.field[i][j].islower():
                    self.draw_text(self.crossword.field[i][j], 48, self.DARKBLUE, 90 + j * 48, 200 + i*48)
                elif self.crossword.field[i][j].isupper():
                    if color:
                        self.draw_text(self.crossword.field[i][j], 48, color, 90 + j * 48, 200 + i*48)
                    else:
                        self.draw_text(self.crossword.field[i][j], 48, self.LIGHTPINK, 90 + j * 48, 200 + i*48)
                
        pygame.display.flip()

    def events(self):
        """
        All events are caught here(including time warp)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    self.quit()
                if event.key == pygame.K_UP:
                    self.TIMESTEP -= 50
                if event.key == pygame.K_DOWN:
                    self.TIMESTEP += 50
    
    def wait_for_key(self):
        """
        Wait for user key press
        """
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(60)
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
    g = Visualization()
    while True:
        g.new()
        g.run()

