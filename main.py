import re
from random import randint
from typing import List, Tuple
from enum import Enum, auto


class Cell:
    def __init__(self):
        self.is_mine: bool = False
        self.is_open: bool = False
        self.mine_around: int = 0

    def __str__(self) -> str:
        return str(self.mine_around)

    def get_value(self) -> int:
        return self.mine_around


class GameField:
    def __init__(self, n: int = 4, m: int = 4, mine_count: int = 4):
        self.__n = n
        self.__m = m
        self.mine_count = mine_count
        self.board: List[List[Cell]] = [[Cell() for _ in range(m)] for _ in range(n)]
        self.end: bool = False
        self.__first_cell: bool = True
        self._generate_mine_on_board()

    @property
    def n(self) -> int:
        return self.__n

    @property
    def m(self) -> int:
        return self.__m

    def _generate_mine_on_board(self):
        mine_located = 0
        while mine_located < self.mine_count:
            x = randint(0, self.__m - 1)
            y = randint(0, self.__n - 1)
            if not self.board[y][x].is_mine:
                self.board[y][x].is_mine = True
                mine_located += 1
        self._calculate_mines()

    def _calculate_mines(self):
        for y in range(self.__n):
            for x in range(self.__m):
                if self.board[y][x].is_mine:
                    continue
                count = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (i != 0 or j != 0) and (0 <= i + y < self.__n and 0 <= j + x < self.__m) and (
                                self.board[i + y][j + x].is_mine):
                            count += 1
                self.board[y][x].mine_around = count

    def _move_mine(self, x: int, y: int):
        self.board[y][x].is_mine = False
        while True:
            nx = randint(0, self.__m - 1)
            ny = randint(0, self.__n - 1)
            if not self.board[ny][nx].is_mine and (nx != x and ny != y):
                self.board[ny][nx].is_mine = True
                break
        self._calculate_mines()

    def open_cell(self, x: int, y: int) -> bool:
        if not (0 <= x < self.__m and 0 <= y < self.__n):
            print("Выход за поле")
            return False

        cell = self.board[y][x]

        if self.__first_cell and cell.is_mine:
            self._move_mine(x, y)
            cell = self.board[y][x]

        self.__first_cell = False

        if cell.is_open:
            return True

        cell.is_open = True

        if cell.is_mine:
            self.end = True
            return False
        elif cell.mine_around == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if (0 <= i + y < self.__n) and (0 <= j + x < self.__m):
                        self.open_cell(j + x, i + y)
        return True

    def end_game(self) -> bool:
        for y in range(self.__n):
            for x in range(self.__m):
                if not self.board[y][x].is_mine and not self.board[y][x].is_open:
                    return False
        return True


class CommandType(Enum):
    OPEN = 'open'
    EXIT = 'exit'
    SHOW = 'show'


class ConsoleInterface:
    @staticmethod
    def get_params() -> Tuple[int, int, int] | None:
        while True:
            try:
                height, width, count = map(int, input("Задайте размер поля и кол-во мин: \nНапример: 2 2 1 \n").split())
                if height <= 0 or width <= 0 or count <= 0:
                    print("Числа должны быть положительные и больше нуля")
                    continue
                if count >= height * width:
                    print("Мин не может быть столько")
                    continue
                return height, width, count
            except ValueError:
                print("Только 3 числа через пробел")

    @staticmethod
    def get_command() -> str | None:
        while True:
            user_input = input("Введите одну из команд:'open x y', 'exit', 'show' \n").strip()
            if not user_input:
                continue

            cmd = user_input.split()
            cmd_name = cmd[0]

            try:
                command: CommandType = CommandType(cmd_name)
            except ValueError:
                print("Неккоректная команда")
                continue

            match command:
                case CommandType.SHOW | CommandType.EXIT:
                    return user_input
                case CommandType.OPEN:
                    try:
                        x = int(cmd[1])
                        y = int(cmd[2])
                        return user_input
                    except ValueError:
                        print("После команды 'open' должны быть 2 числа")
                        continue

    @staticmethod
    def show(game: GameField):
        print(" ".join([str(i) for i in range(game.m + 1)]))
        for y in range(game.n):
            print(y + 1, end=" ")
            for x in range(game.m):
                cell = game.board[y][x]
                if not cell.is_open:
                    print("■", end=" ")
                elif cell.get_value():
                    print(cell.get_value(), end=" ")
                else:
                    print(" ", end=" ")
            print()


def main():
    height, width, count = ConsoleInterface.get_params()
    game = GameField(n=height, m=width, mine_count=count)

    while not game.end:
        cmd = ConsoleInterface.get_command()

        match cmd:
            case cmd if re.fullmatch(r'^exit$', cmd):
                print("Вы вышли")
                break
            case cmd if re.fullmatch(r'^show$', cmd):
                ConsoleInterface.show(game)
            case cmd if (m := re.fullmatch(r'^open\s+(\d+)\s+(\d+)$', cmd)):
                x, y = map(int, m.groups())
                if not game.open_cell(x - 1, y - 1):
                    print("БУМ!!!")
                    ConsoleInterface.show(game)
                    break

        if game.end_game():
            print("Вы победили")
            break


if __name__ == "__main__":
    main()
