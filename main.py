from random import randint


class Minesweeper:
    def __init__(self, n: int = 4, m: int = 4, mine_count: int = 4):
        self.__n = n
        self.__m = m
        self.mine_count = mine_count
        self.board = [[0 for _ in range(m)] for _ in range(n)]
        self.opened_cells = [[False for _ in range(m)] for _ in range(n)]
        self.end = False
        self.__first_cell = True

        # Заполняем минами поле
        mine_located = 0
        while mine_located < mine_count:
            x = randint(0, m - 1)
            y = randint(0, n - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mine_located += 1

        self._calculate_mines()

    # Подсчет мин вокруг
    def _calculate_mines(self):
        for y in range(self.__n):
            for x in range(self.__m):
                if self.board[y][x] == -1:
                    continue
                count = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (i != 0 or j != 0) and (0 <= i + y < self.__n and 0 <= j + x < self.__m) and (
                                self.board[i + y][j + x] == -1):
                            count += 1
                self.board[y][x] = count

    # Перемещаем мину
    def _move_mine(self, x: int, y: int):
        self.board[y][x] = 0

        while True:
            nx = randint(0, self.__m - 1)
            ny = randint(0, self.__n - 1)
            if self.board[ny][nx] != -1 and (nx != x and ny != y):
                self.board[ny][nx] = -1
                break

        self._calculate_mines()

    def open(self, x: int, y: int) -> bool:
        if not (0 <= x < self.__m and 0 <= y < self.__n):
            print("Выход за поле")
            return False

        if self.__first_cell and self.board[y][x] == -1:
            self._move_mine(x, y)

        self.__first_cell = False

        if self.opened_cells[y][x]:
            return True

        self.opened_cells[y][x] = True

        if self.board[y][x] == -1:
            self.end = True
            return False
        elif self.board[y][x] == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if (0 <= i + y < self.__n) and (0 <= j + x < self.__m):
                        self.open(j + x, i + y)
        return True

    def show(self):
        print(" ".join([str(i) for i in range(self.__m + 1)]))
        for y in range(self.__n):
            print(y + 1, end=" ")
            for x in range(self.__m):
                if not self.opened_cells[y][x]:
                    print("■", end=" ")
                elif self.board[y][x]:
                    print(self.board[y][x], end=" ")
                else:
                    print(" ", end=" ")
            print()

    def end_game(self) -> bool:
        for y in range(self.__n):
            for x in range(self.__m):
                if self.board[y][x] != -1 and not self.opened_cells[y][x]:
                    return False
        return True


while True:
    try:
        print("Задайте размер поля и кол-во мин: \nНапример: 2 2 1 ")
        height, width, count = map(int, input().split())
        if height <= 0 or width <= 0 or count <= 0:
            print("Числа должны быть положительные и больше нуля")
            continue
        if count >= height * width:
            print("Мин не может быть столько")
            continue
        break
    except ValueError:
        print("Только 3 числа через пробел")

game = Minesweeper(n=height, m=width, mine_count=count)

while not game.end:
    print("Введите одну из команд:'open x y', 'exit', 'show' ")
    i = list(input().split())

    if i[0] == "exit":
        print("Вы вышли")
        game.end = True

    if i[0] == "show":
        game.show()

    try:
        if i[0] == "open":
            if not game.open(int(i[1]) - 1, int(i[2]) - 1):
                print("Бууум")
                game.end = True
            print("Карта:")
            game.show()
    except ValueError:
        print("Пример команды:'open {цифра} {цифра}'")
        continue

    if game.end_game():
        print("Вы победили")
        game.end = True
