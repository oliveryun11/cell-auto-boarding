import numpy as np, pandas as pd, random, matplotlib.pyplot as plt, seaborn as sns
from IPython.display import clear_output
from PyProbs import Probability as pr

class passenger(object):
    def __init__(self, carry_p, purse_p):
        self.aisle = 0
        self.seat = 0
        self.speed = pr.Prob(3/100)
        self.purse = pr.Prob(purse_p)
        self.carry = pr.Prob(carry_p)
        self.timer = 2
        self.first = 1
        self.action = 0
        self.board = 0
        self.wait = 0
        self.walk = 0
        self.bag = 0

def create_passenger_list(prob, carry_p, purse_p):
    p_list = []
    for i in range(32 * 6):
        p_list.append(passenger(0, 0))
        p_list[i].aisle = i // 6
        p_list[i].seat = i % 6
    both = 0
    purse_o = 0
    carry_o = 0
    for i in range(192):
        a = pr.Prob(purse_p)
        b = pr.Prob(carry_p)
        if a and b:
            both += 1
        elif a:
            purse_o += 1
        elif b:
            carry_o += 1
    ind = 1
    while (both):
        both -= 1
        p_list[-ind].purse = 1
        p_list[-ind].carry = 1
        ind += 1
    while (carry_o):
        carry_o -= 1
        p_list[-ind].carry = 1
        ind += 1
    while (purse_o):
        purse_o -= 1
        p_list[-ind].purse = 1
        ind += 1
    p_list1 = []
    for i in range(32):
        p_list1.append(p_list[6 * i])
    for i in range(32):
        p_list1.append(p_list[6 * i + 5])
    for i in range(32):
        p_list1.append(p_list[6 * i + 1])
    for i in range(32):
        p_list1.append(p_list[6 * i + 4])
    for i in range(32):
        p_list1.append(p_list[6 * i + 2])
    for i in range(32):
        p_list1.append(p_list[6 * i + 3])
    p_list_2 = p_list1[:64]
    p_list_3 = p_list1[64:128]
    p_list_4 = p_list1[128:]
    random.shuffle(p_list_2)
    random.shuffle(p_list_3)
    random.shuffle(p_list_4)
    p_list1[:64] = p_list_2
    p_list1[64:128] = p_list_3
    p_list1[128:] = p_list_4

    i = 0
    fin = 192
    while i < fin:
        if pr.Prob(prob):
            p_list1.append(p_list1.pop(i))
            i -= 1
            fin -= 1
        i += 1
    p_list1.reverse()
    return p_list1

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
prob = 0
carry_p = 0
purse_p = 0
sens = np.zeros((20, 20))
for j in range(-10, 10):
    for k in range(20):
        print(j+10, k)
        time = []
        board_avg = []
        for i in range(1000):
            factor = j * 2 / 100
            prob = k/100
            carry_p = (factor * 50 / 100) + 50/100
            purse_p = (factor * 30 / 100) + 30/100
            p_list = create_passenger_list(prob, carry_p, purse_p)
            p_list = initialize_timer(p_list)
            narrow = [[0] * 8 for _ in range(32)]
            narrow = initialize_array(narrow)
            a, b = run_narrow(p_list, narrow)
            time.append(a)
            #board_avg.append(b)
        sens[j+10][k] = np.mean(time)
        print(sens[j+10][k])
        np.save('our_sens.npy', sens)
print(np.mean(time), np.mean(board_avg))
np_time = np.array(time)
np_board_avg = np.array(board_avg)
#np.save('rp_time.npy', np_time)
#np.save('rp_board_avg.npy', np_board_avg)