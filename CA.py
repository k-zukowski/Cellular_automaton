import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class CA:
    w = 10
    width = 500
    height = 500
    columns = None
    rows = None
    board = None

    def __init__(self):
        self.columns = int(self.width / self.w)
        self.rows = int(self.height / self.w)
        self.board = [[0] * self.columns for _ in range(self.rows)]
        self.board[2][0] = 1
        self.board[3][1] = 1
        self.board[1][2] = 1
        self.board[2][2] = 1
        self.board[3][2] = 1

    def init(self, *args):
        for i in range(self.columns):
            for j in range(self.rows):
                self.board[i][j] = int(random.randint(0, 1))

    def gen(self, rules_in):
        rules_arr = rules_in.split(",")
        st_rule = int(rules_arr[0])
        nd_rule = int(rules_arr[1])
        rd_rule = int(rules_arr[2])
        next_gen = [[0] * self.columns for _ in range(self.rows)]
        for x in range(self.columns):
            for y in range(self.rows):
                neighbours = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        neighbours += self.board[(x + i + self.columns) % self.columns][(y + j + self.rows) % self.rows]
                neighbours -= self.board[x][y]
                if self.board[x][y] == 1 and neighbours < st_rule:  # loneliness
                    next_gen[x][y] = 0
                elif self.board[x][y] == 1 and neighbours > nd_rule:  # overpopulation
                    next_gen[x][y] = 0
                elif self.board[x][y] == 0 and neighbours == rd_rule:  # procreation
                    next_gen[x][y] = 1
                else:
                    next_gen[x][y] = self.board[x][y]  # no change
        self.board = next_gen


rules = "2,3,3"

inp = input("Enter a set of rules you would like to choose from (loneliness|overpopulation|procreation) (2,3,3 4,5,"
            "6) etc.. ").split(" ")
inp.append("2,3,3")
inp.append("1,8,4")
inp.append("1,0,2")

ca = CA()
ca.gen(rules)
data = ca.board
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
im = ax.imshow(data, animated=True)


def press(event):
    global rules
    if event.key == 'enter':
        rand = random.choice(inp)
        while rand == rules:
            rand = random.choice(inp)
        rules = rand
        print(" New rules =", rules)


def update_image(i):
    global rules
    ca.gen(rules)
    next_data = np.array(ca.board)
    im.set_array(next_data)


ani = animation.FuncAnimation(fig, update_image, interval=0)
fig.canvas.mpl_connect('button_press_event', ca.init)
fig.canvas.mpl_connect('key_press_event', press)
plt.show()
