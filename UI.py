import pygame
import time

pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, row, col, w, h, win):
        self.row = row
        self.col = col
        self.w = w
        self.h = h
        self.win = win
        self.cube = [[Cube(self.board[i][j], i, j, w, h) for j in range(col)] for i in range(row)]
        self.model = None
        self.update_model()
        self.selected = None

    def update_model(self):
        self.model = [[self.cube[i][j].value for j in range(self.col)] for i in range(self.row)]

    def place(self, val):
        row, col = self.selected
        if self.cube[row][col].value == 0:
            self.cube[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cube[row][col].set(0)
                self.cube[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cube[row][col].set_temp(val)

    def draw(self):
        gap = self.w / 9
        for i in range(self.row + 1):
            if i != 0 and i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.w, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.h), thick)

        for i in range(self.row):
            for j in range(self.col):
                self.cube[i][j].draw(self.win)

    def select(self, r, c):
        for i in range(self.row):
            for j in range(self.col):
                self.cube[i][j].selected = False

        self.cube[r][c].selected = True
        self.selected = (r, c)

    def clear(self):
        r, c = self.selected
        if self.cube[r][c].value == 0:
            self.cube[r][c].set_temp(0)

    def click(self, pos):
        if pos[0] < self.w and pos[1] < self.h:
            gap = self.w / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.cube[i][j].value == 0:
                    return False

        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            r, c = find

        for i in range(1, 10):
            if valid(self.model, i, (r, c)):
                self.model[r][c] = i
                if self.solve():
                    return True
                self.model[r][c] = 0

        return False

    def solve_ui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            r, c = find

        for i in range(1, 10):
            if valid(self.model, i, (r, c)):
                self.model[r][c] = i
                self.cube[r][c].set(i)
                self.cube[r][c].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_ui():
                    return True

                self.model[r][c] = 0
                self.cube[r][c].set(0)
                self.update_model()
                self.cube[r][c].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, w, h):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.w = w
        self.h = h
        self.selected = False

    def draw(self, win):
        f = pygame.font.SysFont("comicsans", 40)
        gap = self.w / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = f.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = f.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        f = pygame.font.SysFont("comicsans", 40)
        gap = self.w / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = f.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)

    return None


def valid(board, num, pos):
    for i in range(len(board[0])):
        if pos[1] != i and board[pos[0]][i] == num:
            return False

    for i in range(len(board)):
        if pos[0] != i and board[i][pos[1]] == num:
            return False

    x = pos[0] // 3
    y = pos[1] // 3

    for i in range(x * 3, x * 3 + 3):
        for j in range(y * 3, y * 3 + 3):
            if (i, j) != pos and board[i][j] == num:
                return False

    return True


def redraw_win(win, board, time, strikes):
    win.fill((255, 255, 255))
    f = pygame.font.SysFont("comicsans", 40)
    text = f.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    text = f.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    board.draw()


def format_time(secs):
    sec = secs % 60
    min = secs // 60
    hour = min // 60

    return " " + str(min) + ":" + str(sec)


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.solve_ui()
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cube[i][j].temp != 0:
                        if board.place(board.cube[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None
                        if board.is_finished():
                            print("Game Over")
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_win(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
