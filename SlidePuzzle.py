import pygame
import sys
import os
import random
WIDTH = 800  # 視窗寬度
HEIGHT = 600  # 視窗高度
GRID = 4  # 棋盤乘數
BLOCK_SIZE = HEIGHT / GRID  # 方塊寬度
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
FONT_SIZE = 120  # 字體大小


class SlidePuzzle:
    def __init__(self, grid, tiles, margin):
        # grid : n*n 大小遊戲  tiles : 每個方格大小  margin : 距離大小
        self.grid, self.margin = grid, margin
        self.step = 0
        self.tiles = [(x, y) for y in range(grid[1]) for x in range(grid[0])]
        self.finished = [(x, y) for y in range(grid[1])
                         for x in range(grid[0])]
        # self.tiles : 每隔方格順序
        self.tiles_len = grid[0] * grid[1] - 1
        self.tiles_pos = {(x, y): (x * (tiles + margin) + margin, y * (tiles + margin) + margin)
                          for y in range(grid[1]) for x in range(grid[0])}
        # self.tiles_pos : 畫圖順序
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.block = []
        for i in range(self.tiles_len):
            image = pygame.Surface((tiles, tiles))
            image.fill(GREEN)
            text = self.font.render(str(i + 1), True, BLACK)
            center = (tiles - text.get_size()[0]) / 2
            image.blit(text, (center, center))
            self.block.append(image)

    def swap(self, pos):
        n = self.tiles.index(pos)
        self.tiles[n], self.tiles[-1] = self.tiles[-1], self.tiles[n]
        self.step += 1
        print(self.step)

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

    def update(self, times):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:  # 確認是否按下滑鼠
            m_pos = pygame.mouse.get_pos()
            tile = m_pos[0] // BLOCK_SIZE, m_pos[1] // BLOCK_SIZE
            if self.inside(tile):
                if tile in self.adjacent():
                    self.swap(tile)

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
