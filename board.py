import pygame
import random

pygame.init()
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
dark_blue = (0, 0, 102)
brown = (102, 51, 0)
turquoise = (0, 255, 255)
black = (0, 0, 0)
white = (255, 255, 255)
dark_gray = (160, 160, 160)

colors = {
    0: white,
    1: blue,
    2: green,
    3: red,
    4: dark_blue,
    5: brown,
    6: turquoise,
    7: black,
    8: white
}
font = pygame.font.SysFont('arial', 20)


class Board:

    def __init__(self, row, col, mines, size):
        self.row = row
        self.col = col
        self.mines = mines
        self.size = size
        self.first_click = True

        self.board = [[-1] * col for i in range(row)]
        self.open = [[-1] * col for i in range(row)]

    def random_board(self):
        block = [1] * self.mines + ([0] * (self.row * self.col - self.mines - 1))
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j] != 0:
                    val = random.choice(block)
                    self.board[i][j] = val
                    block.remove(val)

    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                if self.open[i][j] != -1:
                    pygame.draw.rect(screen, dark_gray, pygame.Rect(j * self.size, i * self.size, self.size ,self.size ))
                    if self.open[i][j]:
                        num = font.render(f'{self.open[i][j]}', True, colors[self.open[i][j]])
                        screen.blit(num, (j * self.size + 10, i * self.size))

        pygame.display.flip()

    def count(self, x, y):
        if x < 0 or y < 0 or x == self.col or y == self.row or self.open[y][x] != -1:
            return
        count = 0
        if x - 1 > -1:
            count += self.board[y][x - 1]
            if y - 1 > -1:
                count += self.board[y - 1][x - 1]
            if y + 1 < self.row:
                count += self.board[y + 1][x - 1]
        if x + 1 < self.col:
            count += self.board[y][x + 1]
            if y - 1 > -1:
                count += self.board[y - 1][x + 1]
            if y + 1 < self.row:
                count += self.board[y + 1][x + 1]
        if y - 1 > -1:
            count += self.board[y - 1][x]
        if y + 1 < self.row:
            count += self.board[y + 1][x]
        self.open[y][x] = count


    def play(self, x, y):
        if self.first_click:
            self.board[x][y] = 0
            self.random_board()
            self.first_click = False

        seen = [[False] * self.col for i in range(self.row)]

        def play(x, y, flag):
            nonlocal seen
            if x < 0 or y < 0 or x >= self.col or y >= self.row or seen[y][x]:
                return True
            if self.board[y][x]:
                return False
            if not flag:
                return True

            seen[y][x] = True
            check = (
                    play(x - 1, y, False) and
                    play(x + 1, y, False) and
                    play(x, y - 1, False) and
                    play(x, y + 1, False) and
                    play(x - 1, y - 1, False) and
                    play(x - 1, y + 1, False) and
                    play(x + 1, y - 1, False) and
                    play(x + 1, y + 1, False)
            )
            if flag:
                self.count(x, y)
            if check:
                play(x - 1, y, True)
                play(x + 1, y, True)
                play(x, y - 1, True)
                play(x, y + 1, True)
                play(x - 1, y - 1, True)
                play(x - 1, y + 1, True)
                play(x + 1, y - 1, True)
                play(x + 1, y + 1, True)
            return True

        play(x, y, True)
