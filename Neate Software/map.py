import random
from enum import Enum

class Map:
    def __init__(self, x, y):
        self.height = y
        self.width = x
        self.map = []
        for y in range(self.height):
            self.map.append([0]*self.width)
    
    def print(self, p=None):
        for y in range(self.height-1, -1, -1):
            info = []
            for x in range(self.width):
                if p is not None and p[0] == x and p[1] == y:
                    info.append('O')
                elif self.map[y][x] == 0:
                    info.append('.')
                elif self.map[y][x] == -1:
                    info.append('#')
                else:
                    info.append(str(self.map[y][x]))
            print(" ".join(info))
        print('\n')

    def get(self, b):
        if 0 <= b[1] < self.height and 0 <= b[0] < self.width:
            v = self.map[b[1]][b[0]]
        else:
            v = -1
        return v

    def set(self, b, v):
        if 0 <= b[1] < self.height and 0 <= b[0] < self.width:
            if v == 1:
                self.map[b[1]][b[0]] += 1
            else:
                self.map[b[1]][b[0]] = v

    def make_rectangle(self, x, y, w, h):
        origin = (x,y)
        side = (x+w)
        top = (y+h)

        for i in range(y, top):
            for j in range(x, side):
                self.set((j,i), -1)

    def score(self):
        clean = 0
        wall = 0
        redundant = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == -1:
                    wall += 1
                elif self.map[y][x] > 0:
                    clean += 1
                    redundant += self.map[y][x]
        max = (self.height * self.width)-wall
        total = (clean / max)*100
        redun = redundant / clean
        return total, redun


class Bot:
    def __init__(self, x, y, d, m):
        self.x = x
        self.y = y
        self.dir = d
        self.map = m
        self.time_taken = 0

    def copy(self):
        res = Bot(self.x, self.y, self.dir, self.map)
        return res

    def pos(self):
        return (self.x, self.y)

    def next(self, d=None, dis=1):
        dis -= 1
        if d is None:
            d = self.dir
        if d % 2 == 1:
            x = (self.x + dis)+(d & 2)-1
            y = self.y
            self.time_taken += 2
        else:
            x = self.x
            y = (self.y + dis)+(d & 2)-1
            self.time_taken += 2
        return (x,y)

    def fwd(self):
        x,y = self.next()
        self.x = x
        self.y = y
        self.time_taken += 2

    def right(self):
        self.dir = (self.dir + 1) % 4
        self.time_taken += 2

    def left(self):
        self.dir = (self.dir - 1) % 4
        self.time_taken += 2

    def time_passed(self):
        time_taken = self.time_taken
        return time_taken