import pygame
from board import Board
pygame.init()

red = (255, 0, 0)
gray = (220, 230, 230)
black = (0, 0, 0)
white = (255, 255, 255)

size = 20
width = size * 10
height = size * 10
col = width // size
row = height // size
lose = False
f_sys = pygame.font.SysFont('arial', 25, 2)

dis = pygame.display.set_mode((width, height), pygame.RESIZABLE)
board = Board(row , col, 15, size)
dis.fill(gray)
for i in range(col + 1):
    pygame.draw.line(dis, white, (i * size, 0), (i * size, row * size))

for i in range(row + 1):
    pygame.draw.line(dis, white, (0, i * size), (col * size, i * size))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not lose:

            x, y = pygame.mouse.get_pos()
            x, y = x // size, y // size
            if board.board[y][x] == 1:
                text = f_sys.render(f'You Lose', True, red)
                dis.blit(text, (width // 2 , height // 2))
                lose = True
                pygame.display.flip()
            else:
                board.play(x, y)

    board.draw(dis)