import random

COLOR = {1: [(0, 0, 255), '2'], 2: [(0, 255, 0), '4'], 3: [(255, 0, 0), '8'], 4: [(0, 255, 255), '16'], 5: [(255, 255, 0), '32'],
         6: [(255, 100, 255), '64'], 7: [(100, 255, 255), '128'], 8: [(255, 255, 100), '256'], 9: [(100, 255, 100), '512'], 10: [(250, 50, 50), '1K'],
         11: [(50, 50, 250), '2K'], 12: [(255, 50, 255), '4K'], 13: [(255, 255, 50), '8K'], 14: [(50, 255, 255), '16K'], 15: [(50, 150, 200), '32K'],
         16: [(50, 50, 250), '64K'], 17: [(255, 50, 255), '128K'], 18: [(255, 255, 50), '256K'], 19: [(50, 255, 255), '512K'], 20: [(50, 150, 200), '1M']}



class Block:
    def __init__(self, value: int):
        self.value  = value
        self.color = COLOR[value][0]
        self.text = COLOR[value][1]

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __add__(self, other):
        return Block(self.value + 1)


    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return str(self.value)


class BaseGameField:
    def __init__(self):
        self.field = [[None for j in range(7)] for i in range(12)]
        self.status = 0
        self.score = 0
        self.name = 'long'
        self.max_block = 1

    def add_block(self, block: Block, x: int, y: int):

        flag = self.__put_block(block, x, y)
        temp = self.__check_no_windows()
        if temp:
            block, self.field[temp[0]][temp[1]] = self.field[temp[0]][temp[1]], None
            self.add_block(block, temp[0] - 1, temp[1])
        return flag

    def __check_naer_block(self, block, x, y):
        flag = False
        if x and self.field[x - 1][y] and self.field[x - 1][y] == block:
            self.score += self.field[x - 1][y].value
            self.field[x - 1][y] = None
            self.field[x][y] = None
            flag = True
        if y and self.field[x][y - 1] and self.field[x][y - 1] == block:
            self.score += self.field[x][y - 1].value
            self.field[x][y - 1] = None
            flag = True
        if y < 6 and self.field[x][y + 1] and self.field[x][y + 1] == block:
            self.score += self.field[x][y + 1].value
            self.field[x][y + 1] = None
            flag = True
        if flag:
            if self.max_block < 9:
                temp = [i for j in self.field for i in j if i]
                if temp:
                    self.max_block = max(temp).value
            return block + block, flag
        return block, flag

    def __put_block(self, block: Block, x: int, y: int):
        block, flag = self.__check_naer_block(block, x, y)
        if not flag:
            self.field[x][y] = block
        else:
            if x:
                if self.field[x - 1][y] and self.field[x - 1][y] == block:
                    self.field[x][y] = None
                    self.add_block(block + block, x - 1, y)
                elif self.field[x - 1][y] and self.field[x - 1][y] != block:
                    self.field[x][y] = None
                    self.add_block(block, x, y)
                else:
                    self.add_block(block, x - 1, y)
            else:
                self.add_block(block, x, y)
            return flag

    def __check_no_windows(self):
        for y in range(6, -1, -1):
            for x in range(11, 0, -1):
                if self.field[x][y] and self.field[x - 1][y] is None:
                    return (x, y)



    def check_last_field(self):
        return any(self.field[-1])

    def get_free_cell(self, x, y):
        while x:
            if self.field[x - 1][y]:
                return x
            x -= 1
        return x

    def next_status(self):
        self.status = (self.status + 1) % 3

    def game_over(self):
        self.status = 2
        self.field = [[None for j in range(7)] for i in range(12)]


class FastGame(BaseGameField):
    def __init__(self):
        super().__init__()
        self.name = 'fast'
        self.my_init()

    def my_init(self):
        self.field = [[None for j in range(7)] for i in range(12)]
        self.add_row()

    def add_row(self):
        for i in range(11, 0, -1):
            self.field[i] = self.field[i - 1]
        self.field[0] = [Block(random.randint(1, self.max_block)) for _ in range(7)]

    def game_over(self):
        self.status = 2
        self.field = [[None for j in range(7)] for i in range(12)]
        self.add_row()

if __name__ == '__main__':
    Block()
    BaseGameField()
    FastGame()