import pygame
from pygame.locals import *
import sys
import copy
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris", "Tetris")
clock = pygame.time.Clock()
running = True

# 定数
MAX_ROW = 20
MAX_COL = 10
class Block:
    # ブロックの設定
    def __init__(self, block_type):
        self.shapes = [[], [],  # empty block and wall
                       [[0, -1], [0, 0], [0, 1], [0, 2]],  # I block
                       [[-1, -1], [0, -1], [0, 0], [0, 1]],  # J block
                       [[0, -1], [0, 0], [0, 1], [-1, 1]],  # L block
                       [[0, -1], [0, 0], [-1, 0], [-1, 1]],  # S blosk
                       [[-1, -1], [-1, 0], [0, 0], [0, 1]],  # Z block
                       [[0, -1], [0, 0], [-1, 0], [0, 1]],  # T block
                       [[0, 0], [-1, 0], [0, 1], [-1, 1]]]  # square

        self.block_type = block_type
        self.shape = copy.deepcopy(self.shapes[block_type])
        self.row = 1  # initial position
        self.col = 5
        self.level = 0
        self.drop_rate = [60, 50, 45, 42, 39, 36, 35, 34, 33, 32, 31,
                          30, 29, 28, 27, 26, 25, 24, 23, 22, 21,
                          20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
                          10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.count = 60
        self.hold_flag = True

        # ブロック動かすやつ
        def move(self, board, direction):  # direction down:0 left:1 right:2 bottom:3
            if direction == 0 and self.moveable(board, [1, 0]):
                self.row += 1
            elif direction == 1 and self.moveable(board, [0, -1]):
                self.col -= 1
            elif direction == 2 and self.moveable(board, [0, 1]):
                self.col += 1
            elif direction == 3:
                self.row += self.bottom(board)
                self.count = 60

        def bottom(self, board):  #
            direction = [1, 0]
            while self.moveable(board, direction):
                direction[0] += 1
            return direction[0] - 1

        def rotate(self, board, direction):  # clockwise:0 anticloskwise:1
            # 長いバーの回転が異なったら
            if self.block_type == 2:
                if direction == 0:
                    for dx in self.shape:
                        dx[0], dx[1] = dx[1], 1 - dx[0]
                elif direction == 1:
                    for dx in self.shape:
                        dx[0], dx[1] = 1 - dx[1], dx[0]


            # 正方形は回転しない
            elif self.block_type == 8:
                pass

            # 残りのブロック
            elif direction == 0:
                for dx in self.shape:
                    dx[0], dx[1] = dx[1], -dx[0]
            elif direction == 1:
                for dx in self.shape:
                    dx[0], dx[1] = -dx[1], dx[0]

            self.rotate_correction(board)

        # 時間が立ったら勝手に移動
        def drop(self, screen, board):
            if self.count < self.drop_rate[self.level]:
                self.count += 1
                return 0
            elif self.moveable(board, [1, 0]):
                self.count = 0
                self.row += 1
                return 0
            else:
                return 1  # 新しいブロックを作る

        def moveable(self, board, direction):
            drow, dcol = direction

            # ブロックが動けるか判断するやつ
            for dx in self.shape:
                row = self.row + dx[0] + drow
                col = self.col + dx[1] + dcol
                # 移動先を出す
                if 0 <= row < MAX_ROW + 3 and 0 <= col < MAX_COL + 2 and board[row][col] != 0:
                    # 画面外とかだったら動かせないよ
                    return False

            return True

        # ブロック回転したら正しく出来ているかのやつ
        def rotate_correction(self, board):
            move_priority = [[0, 0], [0, -1], [0, 1], [-1, 0], [1, 0], [2, 0], [-1, 1], [1, 1]]
            for direction in move_priority:
                if self.moveable(board, direction):
                    self.row += direction[0]
                    self.col += direction[1]
                    return

            direction = [0, 2]
            while not self.moveable(board, direction):
                direction[1] += 1
            self.row += direction[0]
            self.col += direction[1]

        def draw(self, screen, block_color, board):
            # ドロップしたときの予測
            drow = self.bottom(board)
            for row, col in self.shape:
                row += self.row + drow
                col += self.col
                if row > 1:
                    pygame.draw.rect(screen, block_color[self.block_type],
                                     Rect(30 + 35 * col, 30 + 35 * (row - 2), 35, 35))
                    pygame.draw.rect(screen, block_color[10], Rect(32 + 35 * col, 32 + 35 * (row - 2), 31, 31))

            for row, col in self.shape:
                row += self.row
                col += self.col
                if row > 1:
                    pygame.draw.rect(screen, (0, 0, 0), Rect(30 + 35 * col, 30 + 35 * (row - 2), 35, 35))
                    pygame.draw.rect(screen, block_color[self.block_type],
                                     Rect(32 + 35 * col, 32 + 35 * (row - 2), 31, 31))

        def place(self, screen, board, record):
            for dx in self.shape:
                row = self.row + dx[0]
                col = self.col + dx[1]
                if not (2 <= row < MAX_ROW + 2 and 1 <= col < MAX_COL + 1):  # 画面外にブロックを配置
                    gameover(screen, record)
                    return 1

                board[row][col] = self.block_type
            return 0








while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(60)