import pygame
import sys
import os
import random
from solver_main import A_star
import numpy as np
from solver import Solver
import sys, getopt
from time import sleep
WIDTH = 800  # 視窗寬度
HEIGHT = 600  # 視窗高度
GRID = 3  # 棋盤乘數
BLOCK_SIZE = HEIGHT / GRID  # 方塊寬度
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BRIGHT_RED = (255, 99, 71)
BLUE = (0, 0, 255)
BRIGHT_BLUE = (0, 102, 255)
BRIGHT_GREEN = (144,238,144)
FONT_SIZE = 120  # 字體大小


class SlidePuzzle:
    def __init__(self, grid, tiles, margin):
        # grid : n*n 大小遊戲  tiles : 每個方格大小  margin : 距離大小
        self.times = 1
        self.grid, self.margin = grid, margin
        self.step = 0
        self.tiles = [(x, y) for y in range(grid[1]) for x in range(grid[0])]
        self.finished = [(x, y) for y in range(grid[1])
                         for x in range(grid[0])]
        pic = pygame.image.load('image.jpg')
        pic_width, pic_height = int(grid[0] * (tiles + margin) + margin), int(grid[1] * (tiles + margin) + margin)
        pic = pygame.transform.scale(pic,(pic_width,pic_height))
        # self.tiles : 每隔方格順序
        self.tiles_len = grid[0] * grid[1] - 1
        self.tiles_pos = {(x, y): (x * (tiles + margin) + margin, y * (tiles + margin) + margin)
                          for y in range(grid[1]) for x in range(grid[0])}
        # self.tiles_pos : 畫圖順序
        self.reset = [(x, y) for y in range(grid[1]) for x in range(grid[0])]
        self.solution = []
        self.solutionIndex = 0
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.block = []
        for i in range(self.tiles_len):
            # image = pygame.Surface((tiles, tiles))
            # image.fill(GREEN)
            x, y = self.tiles_pos[self.tiles[i]]
            image = pic.subsurface(x, y, tiles, tiles)
            text = self.font.render(str(i + 1), True, WHITE)
            center = (tiles - text.get_size()[0]) / 2
            image.blit(text, (center, center))
            self.block.append(image)

    def swap(self, pos):
        n = self.tiles.index(pos)
        self.tiles[n], self.tiles[-1] = self.tiles[-1], self.tiles[n]
        self.step += 1

    def adjacent(self):
        x, y = self.tiles[-1]
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

    def inside(self, tile):
        return tile[0] >= 0 and tile[1] >= 0 and tile[0] < self.grid[0]and tile[1] < self.grid[1]

    def random(self, t):
        for _ in range(t):
            i = int(random.random() * 4)
            if self.inside(self.adjacent()[i]):
                self.swap(self.adjacent()[i])
        a = [None] * (GRID * GRID)
        for j in range(GRID * GRID):
            a[j] = self.tiles[j]
        self.reset = a
        self.step = 0

    def update(self, times):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:  # 確認是否按下滑鼠
            m_pos = pygame.mouse.get_pos()
            tile = m_pos[0] // BLOCK_SIZE, m_pos[1] // BLOCK_SIZE
            if self.inside(tile):
                if tile in self.adjacent():
                    self.swap(tile)

    def button(self,msg,x,y,w,h,ic,ac, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))
            if click[0] == 1:
                if msg == "Reset":
                    self.random(100)
                    self.step = 0
                    self.solution = []
                    self.solutionIndex = 0
                elif msg == "Restart":
                    for j in range(GRID * GRID):
                        self.tiles[j] = self.reset[j]
                    self.step = 0
                    self.solution = []
                    self.solutionIndex = 0
                elif msg == "Solve" and not self.checkFinished():
                    if (len(self.solution) is 0):
                        end = [0] * (GRID * GRID)
                        for index in range(1,GRID * GRID):
                            end[index-1] = index
                        end[GRID * GRID - 1] = 0
                        current = [0] * (GRID * GRID)
                        for number in range(1, GRID * GRID):
                            current[self.tiles[number - 1][0] + self.tiles[number - 1][1] * GRID] = number
                        init_state = np.array(current).reshape(GRID, GRID)
                        goal_state = np.array(end).reshape(GRID, GRID)

                        max_iter = 50000
                        heuristic = "manhattan"
                        solution = A_star(init_state, goal_state, max_iter, heuristic)
                        for i in range(len(solution)):
                            self.solution.append(solution[i])
                    else:
                        x, y = self.tiles[-1]
                        if (self.solution[self.solutionIndex] == 0):
                            tile = (x, y + 1)
                        elif (self.solution[self.solutionIndex] == 1):
                            tile = (x, y - 1)
                        elif (self.solution[self.solutionIndex] == 2):
                            tile = (x + 1, y)
                        else:
                            tile = (x - 1, y)
                        self.swap(tile)
                        self.solutionIndex = self.solutionIndex + 1


        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        text_Font = smallText.render(msg, True, WHITE)
        text_Background = text_Font.get_rect()
        text_Background.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(text_Font, text_Background)

    def draw(self, screen):
        for i in range(self.tiles_len):
            x, y = self.tiles_pos[self.tiles[i]]
            screen.blit(self.block[i], (x, y))
        if self.checkFinished():
            font = pygame.font.Font('freesansbold.ttf', 120)
            Win_Font = font.render('You Win', True, WHITE)
            Win_background = Win_Font.get_rect()
            Win_background.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(Win_Font, Win_background)
        s_font = pygame.font.Font('freesansbold.ttf', 30)
        Step_Font = s_font.render('step : ' + str(self.step), True, WHITE)
        Step_background = Step_Font.get_rect()
        Step_background.center = (WIDTH - 70, 20)
        screen.blit(Step_Font, Step_background)
        self.button("Restart", WIDTH - 120, 50, 100, 50, BLUE, BRIGHT_BLUE, screen)
        self.button("Reset", WIDTH - 120, 120, 100, 50, RED, BRIGHT_RED, screen)
        self.button("Solve", WIDTH - 120, 190, 100, 50, GREEN, BRIGHT_GREEN, screen)

    def checkFinished(self):
        return self.tiles == self.finished

    def event(self, e):  # 鍵盤控制
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                x, y = self.tiles[-1]
                tile = (x, y + 1)
                if self.inside(tile):
                    self.swap(tile)
            if e.key == pygame.K_DOWN:
                x, y = self.tiles[-1]
                tile = (x, y - 1)
                if self.inside(tile):
                    self.swap(tile)
            if e.key == pygame.K_LEFT:
                x, y = self.tiles[-1]
                tile = (x + 1, y)
                if self.inside(tile):
                    self.swap(tile)
            if e.key == pygame.K_RIGHT:
                x, y = self.tiles[-1]
                tile = (x - 1, y)
                if self.inside(tile):
                    self.swap(tile)


def main():
    pygame.init()
    pygame.display.set_caption('Slide Puzzle')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((GRID, GRID), BLOCK_SIZE, 5)
    militicks = fpsclock.tick() / 1000
    program.random(100)
    program.step = 0  # 初始化步數

    while True:
        screen.fill(BLACK)
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            program.event(event)
        program.update(militicks)
        pygame.time.wait(50)


if __name__ == "__main__":
    main()
