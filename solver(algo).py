def solve_game(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if check_valid(board, i, (row, col)):
            board[row][col] = i

            if solve_game(board):
                return True

            board[row][col] = 0

    return False


def check_valid(board, num, pos):
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
            if (i, j) != pos and board[i][j]:
                return False

    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)

    return None


def print_board(board):
    for i in range(len(board)):
        if i != 0 and i % 3 == 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j != 0 and j % 3 == 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
