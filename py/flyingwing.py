import numpy as np, pandas as pd, random, matplotlib.pyplot as plt, seaborn as sns
from IPython.display import clear_output
from PyProbs import Probability as pr

class passenger(object):
    def __init__(self):
        self.aisle = 0
        self.seat = 0
        self.speed = 99 - 50*pr.Prob(3/100)
        self.purse = pr.Prob(30/100)
        self.carry = pr.Prob(50/100)
        self.timer = 2
        self.first = 1
        self.action = 0
        self.board = 0
        self.wait = 0
        self.bag = 0
        self.stop_counter = 0
        self.prev_stop = 0


# outside in

def create_passenger_column(seat, r, add, p_list):
    for i in range(r):
        p_list.append(passenger())
        if r == 14:
            p_list[i + add].aisle = i + 1
        else:
            p_list[i + add].aisle = i + 4
        p_list[i + add].seat = seat
    return p_list


def shuffle(add, step, p_list):
    temp = p_list[add:add + step]
    random.shuffle(temp)
    p_list[add:add + step] = temp
    return p_list


def create_side_section(center, p_list, sign, add):
    p_list = create_passenger_column(center - (sign * 3), 14, add + 0, p_list)
    p_list = create_passenger_column(center + (sign * 3), 11, add + 14, p_list)
    p_list = shuffle(add, 25, p_list)
    p_list = create_passenger_column(center - (sign * 2), 14, add + 25, p_list)
    p_list = create_passenger_column(center + (sign * 2), 11, add + 39, p_list)
    p_list = shuffle(add + 25, 25, p_list)
    p_list = create_passenger_column(center - (sign * 1), 14, add + 50, p_list)
    p_list = create_passenger_column(center + (sign * 1), 11, add + 64, p_list)
    p_list = shuffle(add + 50, 25, p_list)
    return p_list


def create_middle_section(center, p_list, add):
    p_list = create_passenger_column(center - (3), 14, add + 0, p_list)
    p_list = create_passenger_column(center + (3), 14, add + 14, p_list)
    p_list = shuffle(add, 28, p_list)
    p_list = create_passenger_column(center - (2), 14, add + 28, p_list)
    p_list = create_passenger_column(center + (2), 14, add + 42, p_list)
    p_list = shuffle(add + 28, 28, p_list)
    p_list = create_passenger_column(center - (1), 14, add + 56, p_list)
    p_list = create_passenger_column(center + (1), 14, add + 70, p_list)
    p_list = shuffle(add + 56, 28, p_list)
    return p_list


def create_passenger_list():
    p_list = []
    # right most
    p_list = create_side_section(24, p_list, 1, 0)
    p_list = create_side_section(3, p_list, -1, 75)
    p_list = create_middle_section(17, p_list, 150)
    p_list = create_middle_section(10, p_list, 234)
    p_list.reverse()
    return p_list

def initialize_timer(p_list):
    for i in range(len(p_list)):
        p_list[i].timer += int(np.random.weibull(2)*(3*p_list[i].purse + 5*p_list[i].carry))
    return p_list

def initialize_array(wing):
    for i in range(4):
        for j in range(14):
            wing[j][i+28] = 12
    return wing

def next_column(wing, i):
    if wing[0][i] != 0:
        if wing[0][i+1] == 0 and wing[0][i].action == 0:
            wing[0][i].prev_stop = 0
            if random.randrange(100) < wing[0][i].speed:
                wing[0][i+1] = wing[0][i]
                wing[0][i] = 0
                wing[0][i+1].action = 1
            else:
                wing[0][i].action = 1
        else:
            if wing[0][i].action == 0:
                wing[0][i].wait += 1
                if wing[0][i].prev_stop == 0:
                    wing[0][i].prev_stop = 1
                    wing[0][i].stop_counter += 1
    return wing

def check_intersection(wing, i):
    if wing[0][i] != 0:
        if i == 3:
            if wing[0][i].seat < 7 and wing[0][i].action == 0 and wing[1][i] == 0:
                wing[1][i] = wing[0][i]
                wing[0][i] = 0
                wing[1][i].action = 1
            elif wing[0][i].seat >= 7 and wing[0][i].action == 0 and wing[0][i+1] == 0:
                wing[0][i+1] = wing[0][i]
                wing[0][i] = 0
                wing[0][i+1].action = 1
            else:
                if wing[0][i].action == 0:
                    if wing[0][i].prev_stop == 0:
                        wing[0][i].prev_stop = 1
                        wing[0][i].stop_counter += 1
                    wing[0][i].wait += 1
                wing[0][i].action = 1
        if i == 10:
            if wing[0][i].seat >= 7 and wing[0][i].seat < 14 and wing[0][i].action == 0 and wing[1][i] == 0:
                wing[1][i] = wing[0][i]
                wing[0][i] = 0
                wing[1][i].action = 1
            elif wing[0][i].seat >= 14 and wing[0][i].action == 0 and wing[0][i+1] == 0:
                wing[0][i+1] = wing[0][i]
                wing[0][i] = 0
                wing[0][i+1].action = 1
            else:
                if wing[0][i].action == 0:
                    if wing[0][i].prev_stop == 0:
                        wing[0][i].prev_stop = 1
                        wing[0][i].stop_counter += 1
                    wing[0][i].wait += 1
                wing[0][i].action = 1
        if i == 17:
            if wing[0][i].seat >= 14 and wing[0][i].seat < 21 and wing[0][i].action == 0 and wing[1][i] == 0:
                wing[1][i] = wing[0][i]
                wing[0][i] = 0
                wing[1][i].action = 1
            elif wing[0][i].seat >= 21 and wing[0][i].action == 0 and wing[0][i+1] == 0:
                wing[0][i+1] = wing[0][i]
                wing[0][i] = 0
                wing[0][i+1].action = 1
            else:
                if wing[0][i].action == 0:
                    if wing[0][i].prev_stop == 0:
                        wing[0][i].prev_stop = 1
                        wing[0][i].stop_counter += 1
                    wing[0][i].wait += 1
                wing[0][i].action = 1
        if i == 24:
            if wing[0][i].action == 0 and wing[1][i] == 0:
                wing[1][i] = wing[0][i]
                wing[0][i] = 0
                wing[1][i].action = 1
            else:
                if wing[0][i].action == 0:
                    if wing[0][i].prev_stop == 0:
                        wing[0][i].prev_stop = 1
                        wing[0][i].stop_counter += 1
                    wing[0][i].wait += 1
                wing[0][i].action = 1
    return wing

def check_aisle(wing, i, j):
    if wing[i][j].seat == j - 3:
        wing[i][j].timer += 5*wing[i][j-2] + 3*wing[i][j-1]
    if wing[i][j].seat == j + 3:
        wing[i][j].timer += 5*wing[i][j+2] + 3*wing[i][j+1]
    if wing[i][j].seat == j - 2:
        wing[i][j].timer += 3*wing[i][j-1]
    if wing[i][j].seat == j + 2:
        wing[i][j].timer += 3*wing[i][j+1]
    return wing[i][j]

def update_column(wing, column, sit, seated):
    for i in range(1, 15):
            if wing[i][column] != 0:
                if wing[i][column].aisle != i:
                    if wing[i+1][column] == 0 and wing[i][column].action == 0:
                        wing[i][column].action = 1
                        wing[i][column].prev_stop = 0
                        if random.randrange(100) < wing[i][column].speed:
                            wing[i+1][column] = wing[i][column]
                            wing[i][column] = 0
                    elif wing[i][column].action == 0:
                        if wing[i][column].prev_stop == 0:
                            wing[i][column].prev_stop = 1
                            wing[i][column].stop_counter += 1
                        wing[i][column].wait += 1
                else:
                    if wing[i][column].first:
                        wing[i][column].first = 0
                        if column == 3:
                            wing[i][28] -= (wing[i][column].purse + 2*wing[i][column].carry)
                            if wing[i][28] < 0:
                                wing[i][column].timer += 5
                        elif column == 10:
                            wing[i][29] -= (wing[i][column].purse + 2*wing[i][column].carry)
                            if wing[i][29] < 0:
                                wing[i][column].timer += 5
                        elif column == 17:
                            wing[i][30] -= (wing[i][column].purse + 2*wing[i][column].carry)
                            if wing[i][30] < 0:
                                wing[i][column].timer += 5
                        elif column == 24:
                            wing[i][31] -= (wing[i][column].purse + 2*wing[i][column].carry)
                            if wing[i][31] < 0:
                                wing[i][column].timer += 5
                        wing[i][column] = check_aisle(wing, i, column)
                        if wing[i][column].speed == 49:
                            wing[i][column].timer *= 2
                        wing[i][column].bag = wing[i][column].timer
                    if wing[i][column].timer != 0:
                        wing[i][column].timer -= 1
                    else:
                        wing[i][wing[i][column].seat] = 1
                        seated.append(wing[i][column])
                        wing[i][column] = 0
                        sit += 1
    return wing, sit, seated

def reset_action(wing):
    for i in range(25):
        if wing[0][i] != 0:
            wing[0][i].action = 0
            wing[0][i].board += 1
    for i in range(3, 25, 7):
        for j in range(1, 15):
            if wing[j][i] != 0:
                wing[j][i].action = 0
                wing[j][i].board += 1
    return wing

def plot_fig(wing, viewer, time, sit, a):
    for i in range(15):
        for j in range(28):
            if wing[i][j] != 0:
                if wing[i][j] == 1:
                    viewer[i][j] = 10
                else:
                    if wing[i][j].speed == 49:
                        viewer[i][j] = 3
                    else:
                        viewer[i][j] = 10
            else:
                if j == 3 or j == 10 or j == 17 or j == 24 or i == 0:
                    viewer[i][j] = 0
                else:
                    viewer[i][j] = 5
    plt.close()
    fig, ax = plt.subplots()
    im = ax.imshow(viewer, cmap = 'summer', vmin = 0, vmax = 10)

    if time % 5 == 0 or sit == 318:
        #plt.savefig('flyingwingoustidein_' + str(a) +'.pdf')
        a += 1
    plt.draw()
    print(sit)
    plt.pause(0.0000001)
    return a

def run_wing(wing, p_list):
    sit = 0
    time = 0
    a = 0
    seated = []
    viewer = [[0] * 28 for _ in range(15)]
    while sit < 318:
        time += 1
        if wing[0][0] == 0 and len(p_list) != 0:
            wing[0][0] = p_list.pop()
            wing[0][0].action = 1
            change = 1
        for i in range(3):
            wing = next_column(wing, i)
        wing = check_intersection(wing, 3)
        wing, sit, seated = update_column(wing, 3, sit, seated)
        for i in range(4, 10):
            wing = next_column(wing, i)
        wing = check_intersection(wing, 10)
        wing, sit, seated = update_column(wing, 10, sit, seated)
        for i in range(11, 17):
            wing = next_column(wing, i)
        wing = check_intersection(wing, 17)
        wing, sit, seated = update_column(wing, 17, sit, seated)
        for i in range(18, 24):
            wing = next_column(wing, i)
        wing = check_intersection(wing, 24)
        wing, sit, seated = update_column(wing, 24, sit, seated)
        wing = reset_action(wing)
        a = plot_fig(wing, viewer, time, sit, a)
    board_time = []
    wait_time = []
    bag_time = []
    stop_counter = []
    for i in range(len(seated)):
        board_time.append(seated[i].board)
        wait_time.append(seated[i].wait)
        bag_time.append(seated[i].bag)
        stop_counter.append(seated[i].stop_counter)
    return time, np.mean(board_time), np.mean(wait_time), np.mean(bag_time), np.mean(stop_counter)

time = []
board_avg = []
wait_avg = []
bag_avg = []
stop_avg = []
for i in range(1):
    print(i)
    p_list = create_passenger_list()
    p_list = initialize_timer(p_list)
    wing = [[0] * 32 for _ in range(15)]
    wing = initialize_array(wing)
    a, b, c, d, e = run_wing(wing, p_list)
    time.append(a)
    board_avg.append(b)
    wait_avg.append(c)
    bag_avg.append(d)
    stop_avg.append(e)

print(np.mean(time), np.mean(board_avg), np.mean(wait_avg), np.mean(bag_avg), np.mean(stop_avg))
np_time = np.array(time)
np_board_avg = np.array(board_avg)
np_wait_avg = np.array(wait_avg)
np_bag_avg = np.array(bag_avg)
np_stop_avg = np.array(stop_avg)
np.save('sec_fw_time.npy', np_time)
np.save('sec_fw_board_avg.npy', np_board_avg)
np.save('sec_fw_wait_avg.npy', np_wait_avg)
np.save('sec_fw_bag_avg.npy', np_bag_avg)
np.save('sec_fw_stop_avg.npy', np_stop_avg)