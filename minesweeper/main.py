from pygame.locals import *
from random import randint
import pygame
import os

os.system('clear')

class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.uncovered = False
        self.flagged = False
        self.type = None

        self.exploded_img = pygame.image.load('images/exploded.png')
        self.hidden_img = pygame.image.load('images/blank.png')
        self.flag_img = pygame.image.load('images/flagged.png')
        self.img_0 = pygame.image.load('images/0.png')
        self.img_1 = pygame.image.load('images/1.png')
        self.img_2 = pygame.image.load('images/2.png')
        self.img_3 = pygame.image.load('images/3.png')
        self.img_4 = pygame.image.load('images/4.png')
        self.img_5 = pygame.image.load('images/5.png')
        self.img_6 = pygame.image.load('images/6.png')
        self.img_7 = pygame.image.load('images/7.png')
        self.img_8 = pygame.image.load('images/8.png')

    def render(self, surface):
        if self.flagged:
            surface.blit(self.flag_img, (self.x, self.y))
        elif not self.uncovered:
            surface.blit(self.hidden_img, (self.x, self.y))
        elif self.type == 0:
            surface.blit(self.img_0, (self.x, self.y))
        elif self.type == 1:
            surface.blit(self.img_1, (self.x, self.y))
        elif self.type == 2:
            surface.blit(self.img_2, (self.x, self.y))
        elif self.type == 3:
            surface.blit(self.img_3, (self.x, self.y))
        elif self.type == 4:
            surface.blit(self.img_4, (self.x, self.y))
        elif self.type == 5:
            surface.blit(self.img_5, (self.x, self.y))
        elif self.type == 6:
            surface.blit(self.img_6, (self.x, self.y))
        elif self.type == 7:
            surface.blit(self.img_7, (self.x, self.y))
        elif self.type == 8:
            surface.blit(self.img_8, (self.x, self.y))
        elif self.type == 'bomb':
            surface.blit(self.exploded_img, (self.x, self.y))


class Game:
    def __init__(self):
        self.resolution = (480, 240)
        self.running = True
        self.clock = pygame.time.Clock()
        self.firstClick = True

        self.blockSetup()

        pygame.init()
        self.display_surf = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('Minesweeper')

    def blockSetup(self):
        step = 16
        x = 0
        y = 0
        self.blocks = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        for i in range(15):
            for b in range(30):
                self.blocks[i].append(1)
                self.blocks[i][b] = Grid(x, y)
                x += step
            y += step
            x = 0

        # Randomize bombs
        self.bombs = 50
        new_bombs = []
        for i in range(self.bombs):
            bomb = [randint(0, 29), randint(0, 14)]
            if not bomb in new_bombs:
                new_bombs.append(bomb)
                self.blocks[bomb[1]][bomb[0]].type = 'bomb'
            else:
                while bomb in new_bombs:
                    bomb = [randint(0, 29), randint(0, 14)]
                new_bombs.append(bomb)
                self.blocks[bomb[1]][bomb[0]].type = 'bomb'

        # Do the Numbering
        for column in range(30):
            for row in range(15):
                if not self.blocks[row][column].type == 'bomb':
                    bomb_count = 0
                    if row + 1 != 15:
                        if self.blocks[row+1][column].type == 'bomb':
                            bomb_count += 1

                    if row + 1 != 15 and column + 1 != 30:
                        if self.blocks[row+1][column+1].type == 'bomb':
                            bomb_count += 1

                    if column + 1 != 30:
                        if self.blocks[row][column+1].type == 'bomb':
                            bomb_count += 1

                    if row - 1 != -1 and column + 1 != 30:
                        if self.blocks[row-1][column+1].type == 'bomb':
                            bomb_count += 1

                    if row - 1 != -1:
                        if self.blocks[row-1][column].type == 'bomb':
                            bomb_count += 1

                    if row - 1 != -1 and column - 1 != -1:
                        if self.blocks[row-1][column-1].type == 'bomb':
                            bomb_count += 1

                    if column - 1 != -1:
                        if self.blocks[row][column-1].type == 'bomb':
                            bomb_count += 1

                    if row + 1 != 15 and column - 1 != -1:
                        if self.blocks[row+1][column-1].type == 'bomb':
                            bomb_count += 1

                    self.blocks[row][column].type = bomb_count

    def render(self):
        self.display_surf.fill((192, 192, 192))
        for i in self.blocks:
            for b in i:
                b.render(self.display_surf)
        pygame.display.flip()

    def clearAround(self, x, y):
        if y + 1 < 15:
            if not self.blocks[y+1][x].uncovered:
                self.blocks[y + 1][x].uncovered = True
                if self.blocks[y + 1][x].type == 0:
                    self.clearAround(x, y + 1)


        if y + 1 < 15 and x + 1 < 30:
            if not self.blocks[y+1][x+1].uncovered:
                self.blocks[y + 1][x + 1].uncovered = True
                if self.blocks[y + 1][x + 1].type == 0:
                    self.clearAround(x + 1, y + 1)


        if x + 1 < 30:
            if not self.blocks[y][x+1].uncovered:
                self.blocks[y][x + 1].uncovered = True
                if self.blocks[y][x + 1].type == 0:
                    self.clearAround(x + 1, y)


        if y - 1 > -1 and x + 1 < 30:
            if not self.blocks[y-1][x+1].uncovered:
                self.blocks[y - 1][x + 1].uncovered = True
                if self.blocks[y - 1][x + 1].type == 0:
                    self.clearAround(x + 1, y - 1)


        if y - 1 > -1:
            if not self.blocks[y-1][x].uncovered:
                self.blocks[y - 1][x].uncovered = True
                if self.blocks[y - 1][x].type == 0:
                    self.clearAround(x, y - 1)


        if y - 1 > -1 and x - 1 > -1:
            if not self.blocks[y-1][x-1].uncovered:
                self.blocks[y - 1][x - 1].uncovered = True
                if self.blocks[y - 1][x - 1].type == 0:
                    self.clearAround(x - 1, y - 1)


        if x - 1 > -1:
            if not self.blocks[y][x-1].uncovered:
                self.blocks[y][x - 1].uncovered = True
                if self.blocks[y][x - 1].type == 0:
                    self.clearAround(x - 1, y)


        if y + 1 < 15 and x - 1 > -1:
            if not self.blocks[y+1][x-1].uncovered:
                self.blocks[y + 1][x - 1].uncovered = True
                if self.blocks[y + 1][x - 1].type == 0:
                    self.clearAround(x - 1, y + 1)

    def gameOver(self):
        self.running = False

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]
                    x = int(x / 16)
                    y = int(y / 16)
                    if self.firstClick and self.blocks[y][x].type != 0:
                        self.firstClick = False
                        while self.blocks[y][x].type != 0:
                            self.blockSetup()
                    elif self.firstClick:
                        self.firstClick = False

                    if not self.blocks[y][x].uncovered and not self.blocks[y][x].flagged:
                        self.blocks[y][x].uncovered = True
                        if self.blocks[y][x].type == 0:
                            self.clearAround(x, y)

                        if self.blocks[y][x].type == 'bomb':
                            self.gameOver()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and not self.firstClick:
                    x = event.pos[0]
                    y = event.pos[1]
                    x = int(x / 16)
                    y = int(y / 16)
                    if self.blocks[y][x].flagged:
                        self.blocks[y][x].flagged = False
                    elif not self.blocks[y][x].uncovered:
                        self.blocks[y][x].flagged = True

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self.running = False

            self.render()
            self.clock.tick(100)

        pygame.quit()


game = Game()
game.loop()
