import numpy as np, pandas as pd, random, matplotlib.pyplot as plt, seaborn as sns
from IPython.display import clear_output
from PyProbs import Probability as pr

class passenger(object):
    def __init__(self, purse_prob, carry_prob):
        self.aisle = 0
        self.seat = 0
        self.speed = pr.Prob(3/100)
        self.purse = purse_prob
        self.carry = carry_prob
        self.timer = 2
        self.first = 1
        self.action = 0
        self.board = 0

def create_passenger_list(purse_prob, carry_prob, percentage):
    p_list = []
    for i in range(4):
        for j in range(48):
            p_list.append(passenger(purse_prob, carry_prob))
            if i == 0:
                if j%2 == 0:
                    p_list[48*i+j].seat = 0
                else:
                    p_list[48*i+j].seat = 5
                p_list[48*i+j].aisle = 31 - j//2
            if i == 1:
                if j < 16:
                    if j%2 == 0:
                        p_list[48*i+j].seat = 0
                    else:
                        p_list[48*i+j].seat = 5
                    p_list[48*i+j].aisle = 31 - (j//2 + 24)
                else:
                    if j%2 == 0:
                        p_list[48*i+j].seat = 1
                    else:
                        p_list[48*i+j].seat = 4
                    p_list[48*i+j].aisle = 31 - (j//2-8)
            if i == 2:
                if j < 32:
                    if j%2 == 0:
                        p_list[48*i+j].seat = 1
                    else:
                        p_list[48*i+j].seat = 4
                    p_list[48*i+j].aisle = 31 - (j//2 + 16)
                else:
                    if j%2 == 0:
                        p_list[48*i+j].seat = 2
                    else:
                        p_list[48*i+j].seat = 3
                    p_list[48*i+j].aisle = 31 - (j//2 - 16)
            if i == 3:
                if j%2 == 0:
                    p_list[48*i+j].seat = 2
                else:
                    p_list[48*i+j].seat = 3
                p_list[48*i+j].aisle = 31 - (j//2 + 8)
    p_list_1 = p_list[:48]
    p_list_2 = p_list[48:96]
    p_list_3 = p_list[96:144]
    p_list_4 = p_list[144:]
    random.shuffle(p_list_1)
    random.shuffle(p_list_2)
    random.shuffle(p_list_3)
    random.shuffle(p_list_4)
    p_list[:48] = p_list_1
    p_list[48:96] = p_list_2
    p_list[96:144] = p_list_3
    p_list[144:] = p_list_4
    fin = 192
    i = 0
    while i < fin:
        if pr.Prob(percentage):
            p_list.append(p_list.pop(i))
            i -= 1
            fin -= 1
    p_list.reverse()
    return p_list

def initialize_array(narrow):
    for i in range(32):
        narrow[i][7] = 12
    return narrow

def initialize_timer(p_list):
    for i in range(len(p_list)):
        p_list[i].timer += 3*p_list[i].purse + 5*p_list[i].carry
        if p_list[i].speed:
            p_list[i].speed = 49
        else:
            p_list[i].speed = 99
    return p_list

def run_narrow(p_list, narrow):
    plt.close("all")
    #fig, ax = plt.subplots()
    #plt.ion()
    #plt.show()
    sit = 0
    time = 0
    seated = []
    viewer = zeros = [[0] * 7 for _ in range(32)]
    while sit < 191:
        time += 1
        for i in range(32):
            change = 0
            if narrow[i][3] != 0 and narrow[i][3].action == 0:
                narrow[i][3].action = 1
                if narrow[i][3].aisle != i:
                    if narrow[i+1][3] == 0:
                        if random.randrange(100) < narrow[i][3].speed:
                            narrow[i+1][3] = narrow[i][3]
                            narrow[i][3] = 0
                            change = 1
                else:
                    if narrow[i][3].first:
                        narrow[i][3].first = 0
                        narrow[i][7] -= narrow[i][3].purse + narrow[i][3].carry
                        if narrow[i][7] < 0:
                            narrow[i][3].timer += 5
                        if narrow[i][3].aisle == 0:
                            narrow[i][3].timer += 5*narrow[i][1] + 3*narrow[i][2]
                        elif narrow[i][3].aisle == 1:
                            narrow[i][3].timer += 3*narrow[i][2]
                        elif narrow[i][3].aisle == 5:
                            narrow[i][3].timer += 3*narrow[i][4]
                        elif narrow[i][3].aisle == 6:
                            narrow[i][3].timer += 5*narrow[i][5] + 3*narrow[i][4]
                        if narrow[i][3].speed == 49:
                            narrow[i][3].timer *= 2
                    if narrow[i][3].timer != 0:
                        narrow[i][3].timer -= 1
                    else:
                        change = 1
                        if narrow[i][3].seat >= 3:
                            narrow[i][narrow[i][3].seat + 1] = 1
                            sit += 1
                        else:
                            narrow[i][narrow[i][3].seat] = 1
                            sit += 1
                        seated.append(narrow[i][3])
                        narrow[i][3] = 0
            if i == 0:
                if narrow[i][3] == 0 and len(p_list) != 0:
                    narrow[i][3] = p_list.pop()
                    narrow[i][3].action = 1
                    change = 1
            """
            if change:
                for i in range(32):
                    for j in range(7):
                        if narrow[i][j] != 0:
                            if j != 3:
                                viewer[i][j] = 2
                            else:
                                if narrow[i][j].speed == 49:
                                    viewer[i][j] = 7
                                else:
                                    viewer[i][j] = 10
                        else:
                            viewer[i][j] = 0
                plt.close()
                fig, ax = plt.subplots()
                im = ax.imshow(viewer)
                plt.draw()
                plt.pause(0.0000001)
                """
        for i in range(32):
            if narrow[i][3] != 0:
                narrow[i][3].action = 0
                narrow[i][3].board += 1
    board_time = []
    for i in range(len(seated)):
        board_time.append(seated[i].board)
    return time, np.mean(board_time)
time = []
board_avg = []
purse_prob = 30/100
carry_prob = 50/100
percentage = 0
sens = np.zeros((20, 20))
for j in range(-10, 10):
    for k in range(20):
        for i in range(1000):
            factor = j*2/100
            purse_prob = (factor * 30 / 100) + 30/100
            carry_prob = (factor * 50 / 100) + 50/100
            percentage = k/100
            print(percentage, purse_prob, carry_prob)
            p_list = create_passenger_list(purse_prob, carry_prob, percentage)
            p_list = initialize_timer(p_list)
            narrow = [[0] * 8 for _ in range(32)]
            narrow = initialize_array(narrow)
            a, b = run_narrow(p_list, narrow)
            time.append(a)
            board_avg.append(b)
        sens[j+10][k] = np.mean(time)
        np.save('sens.npy', sens)
print(np.mean(time), np.mean(board_avg))
np_time = np.array(time)
np_board_avg = np.array(board_avg)
#np.save('rp_time.npy', np_time)
#np.save('rp_board_avg.npy', np_board_avg)