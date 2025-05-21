import random
from typing import List, Tuple

class Minesweeper:
    def __init__(self, width: int = 9, height: int = 9, mines: int = 10):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.visible = [[False for _ in range(width)] for _ in range(height)]
        self.flags = [[False for _ in range(width)] for _ in range(height)]
        self._generate_board()
        self.remaining = width * height - mines

    def _generate_board(self) -> None:
        positions = [(r, c) for r in range(self.height) for c in range(self.width)]
        for r, c in random.sample(positions, self.mines):
            self.board[r][c] = -1
            for rr in range(max(0, r-1), min(self.height, r+2)):
                for cc in range(max(0, c-1), min(self.width, c+2)):
                    if self.board[rr][cc] != -1:
                        self.board[rr][cc] += 1

    def display(self) -> None:
        header = '   ' + ' '.join(f'{i}' for i in range(self.width))
        print(header)
        for r in range(self.height):
            row = []
            for c in range(self.width):
                if self.flags[r][c]:
                    row.append('F')
                elif not self.visible[r][c]:
                    row.append('.')
                else:
                    val = self.board[r][c]
                    row.append('*' if val == -1 else (str(val) if val > 0 else ' '))
            print(f'{r:2} ' + ' '.join(row))

    def open_cell(self, r: int, c: int) -> bool:
        if not (0 <= r < self.height and 0 <= c < self.width):
            print('Coordinates out of bounds')
            return True
        if self.flags[r][c] or self.visible[r][c]:
            return True
        if self.board[r][c] == -1:
            self.visible[r][c] = True
            print('Boom! You hit a mine.')
            return False
        self._reveal(r, c)
        return True

    def _reveal(self, r: int, c: int) -> None:
        stack = [(r, c)]
        while stack:
            rr, cc = stack.pop()
            if self.visible[rr][cc]:
                continue
            self.visible[rr][cc] = True
            self.remaining -= 1
            if self.board[rr][cc] == 0:
                for nr in range(max(0, rr-1), min(self.height, rr+2)):
                    for nc in range(max(0, cc-1), min(self.width, cc+2)):
                        if not self.visible[nr][nc] and self.board[nr][nc] != -1:
                            stack.append((nr, nc))

    def toggle_flag(self, r: int, c: int) -> None:
        if not (0 <= r < self.height and 0 <= c < self.width):
            print('Coordinates out of bounds')
            return
        if self.visible[r][c]:
            return
        self.flags[r][c] = not self.flags[r][c]

    def check_win(self) -> bool:
        return self.remaining == 0

def main():
    game = Minesweeper()
    while True:
        game.display()
        try:
            cmd = input('Enter command (o row col to open, f row col to flag): ').strip().split()
        except EOFError:
            print()
            break
        if not cmd:
            continue
        if cmd[0].lower() in ['o', 'open'] and len(cmd) == 3:
            try:
                r, c = int(cmd[1]), int(cmd[2])
            except ValueError:
                print('Invalid coordinates')
                continue
            if not game.open_cell(r, c):
                game.display()
                print('Game over!')
                break
            if game.check_win():
                game.display()
                print('Congratulations, you cleared the board!')
                break
        elif cmd[0].lower() in ['f', 'flag'] and len(cmd) == 3:
            try:
                r, c = int(cmd[1]), int(cmd[2])
            except ValueError:
                print('Invalid coordinates')
                continue
            game.toggle_flag(r, c)
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()
