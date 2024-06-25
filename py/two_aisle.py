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
        self.path = 0


def shuffle(add, step, p_list):
    temp = p_list[add:add+step]
    random.shuffle(temp)
    p_list[add:add+step] = temp
    return p_list

def create_passenger_list():
    p_list = []
    p_list_2 = []
    i = 0
    ind = 0
    while i < 22:
        if i != 0 and i != 15 and i != 16 and i != 18:
            p_list.append(passenger())
            p_list[ind].aisle = i
            p_list[ind].seat = 0
            ind += 1
            p_list.append(passenger())
            p_list[ind].aisle = i
            p_list[ind].seat = 1
            ind += 1
            if i != 1 and i != 17:
                p_list.append(passenger())
                p_list[ind].aisle = i
                p_list[ind].seat = 3
                ind += 1
                p_list.append(passenger())
                p_list[ind].aisle = i
                p_list[ind].seat = 4
                if i%2 == 0:
                    p_list[ind].path = 1
                ind += 1
                p_list.append(passenger())
                p_list[ind].aisle = i
                p_list[ind].seat = 5
                p_list[ind].path = 1
                ind += 1
            p_list.append(passenger())
            p_list[ind].aisle = i
            p_list[ind].seat = 7
            p_list[ind].path = 1
            ind += 1
            p_list.append(passenger())
            p_list[ind].aisle = i
            p_list[ind].seat = 8
            p_list[ind].path = 1
            ind += 1
        i += 1
    i = 22
    ind = 0
    while i < 42:
        if i != 40 and i != 41:
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 0
            ind += 1
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 1
            ind += 1
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 3
            ind += 1
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 4
            if i%2 == 0:
                p_list_2[ind].path = 1
            ind += 1
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 5
            p_list_2[ind].path = 1
            ind += 1
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 7
            p_list_2[ind].path = 1
            ind += 1
            p_list_2.append(passenger())
            p_list_2[ind].aisle = i
            p_list_2[ind].seat = 8
            p_list_2[ind].path = 1
            ind += 1
        i += 1
    return p_list, p_list_2
def initialize_passenger_list(p_list_1, p_list_2):
    for i in range(len(p_list_1)):
        p_list_1[i].timer += int(np.random.weibull(2) * (3 * p_list_1[i].purse + 5 * p_list_1[i].carry))
    for i in range(len(p_list_2)):
        p_list_2[i].timer += int(np.random.weibull(2) * (3 * p_list_2[i].purse + 5 * p_list_2[i].carry))
    return p_list_1, p_list_2

def initialize_array(two):
    for i in range(42):
        two[9][i] = 6
        two[10][i] = 6
    return two

def next_row(two, i, j):
    if two[i][j] != 0:
        if two[i + 1][j] == 0 and two[i][j].action == 0:
            two[i][j].action = 1
            two[i][j].prev_stop = 0
            if random.randrange(100) < two[i][j].speed:
                two[i+1][j] = two[i][j]
                two[i][j] = 0
        else:
            if two[i][j].action == 0:
                two[i][j].wait += 1
                if two[i][j].prev_stop == 0:
                    two[i][j].prev_stop = 1
                    two[i][j].stop_counter += 1
    return two


def check_intersect(two, i, j, sign):
    if two[i][j] != 0:
        if two[i][j].action == 0:
            two[i][j].action = 1
            if two[i][j].path == 0:
                if two[i][j + (sign*1)] == 0:
                    two[i][j].prev_stop = 0
                    if random.randrange(100) < two[i][j].speed:
                        two[i][j + (sign*1)] = two[i][j]
                        two[i][j] = 0
                else:
                    two[i][j].wait += 1
                    if two[i][j].prev_stop == 0:
                        two[i][j].prev_stop = 1
                        two[i][j].stop_counter += 1
            else:
                if two[i+1][j] == 0:
                    two[i][j].prev_stop = 0
                    if random.randrange(100) < two[i][j].speed:
                        two[i+1][j] = two[i][j]
                        two[i][j] = 0
                else:
                    two[i][j].wait += 1
                    if two[i][j].prev_stop == 0:
                        two[i][j].prev_stop = 1
                        two[i][j].stop_counter += 1
    return two

def check_intersect_2(two, i, j, sign):
    if two[i][j] != 0:
        if two[i][j].action == 0:
            two[i][j].action = 1
            if two[i][j+(sign*1)] == 0:
                two[i][j].prev_stop = 0
                if random.randrange(100) < two[i][j].speed:
                    two[i][j+(sign*1)] = two[i][j]
                    two[i][j] = 0
            else:
                two[i][j].wait += 1
                if two[i][j].prev_stop == 0:
                    two[i][j].prev_stop = 1
                    two[i][j].stop_counter += 1
    return two
def check_aisle(two, i, j):
    if two[i][j].seat == 0:
        two[i][j].timer += 3*two[1][j]

    if two[i][j].seat == 8:
        two[i][j].timer += 3*two[7][j]

    if two[i][j].seat == 4:
        if two[i][j].path == 0:
            two[i][j].timer += 3*two[3][j]

        else:

            two[i][j].timer += 3*two[5][j]
    return two[i][j]

def check_right(two, row, sit, seated):
    for i in range(40, 21, -1):
        if two[row][i] != 0:
            if two[row][i].aisle != i:
                if two[row][i-1] == 0 and two[row][i].action == 0:
                    two[row][i].action = 1
                    two[row][i].prev_stop = 0
                    if random.randrange(100) < two[row][i].speed:
                        two[row][i-1] = two[row][i]
                        two[row][i] = 0
                else:
                    if two[row][i].action == 0:
                        two[row][i].wait += 1
                        if two[row][i].prev_stop == 0:
                            two[row][i].prev_stop = 1
                            two[row][i].stop_counter += 1
            else:
                if two[row][i].first:
                    two[row][i].first = 0
                    if row == 2:
                        two[9][i] -= (two[row][i].purse + 2*two[2][i].carry)
                        if two[9][i] < 0:
                            two[2][i].timer += 5
                    else:
                        two[10][i] -= (two[6][i].purse + 2 * two[6][i].carry)
                        if two[10][i] < 0:
                            two[6][i].timer += 5
                    two[row][i] = check_aisle(two, row, i)
                    if two[row][i].speed == 49:
                        two[row][i].timer *= 2
                    two[row][i].bag = two[row][i].timer
                if two[row][i].action == 0 and two[row][i].timer != 0:
                    two[row][i].action = 1
                    two[row][i].timer -= 1
                else:
                    two[two[row][i].seat][i] = 1
                    seated.append(two[row][i])
                    sit += 1
                    two[row][i] = 0
    return two, sit, seated


def check_left(two, row, sit, seated):
    for i in range(1, 22):
        if two[row][i] != 0:
            if two[row][i].aisle != i:
                if two[row][i + 1] == 0 and two[row][i].action == 0:
                    two[row][i].action = 1
                    two[row][i].prev_stop = 0
                    if random.randrange(100) < two[row][i].speed:
                        two[row][i + 1] = two[row][i]
                        two[row][i] = 0
                else:
                    if two[row][i].action == 0:
                        two[row][i].wait += 1
                        if two[row][i].prev_stop == 0:
                            two[row][i].prev_stop = 1
                            two[row][i].stop_counter += 1
            else:
                if two[row][i].first:
                    two[row][i].first = 0
                    if row == 2:
                        two[9][i] -= (two[2][i].purse + 2 * two[2][i].carry)
                        if two[9][i] < 0:
                            two[2][i].timer += 5
                    else:
                        two[10][i] -= (two[6][i].purse + 2 * two[6][i].carry)
                        if two[10][i] < 0:
                            two[6][i].timer += 5
                    two[row][i] = check_aisle(two, row, i)
                    if two[row][i].speed == 49:
                        two[row][i].timer *= 2
                    two[row][i].bag = two[row][i].timer
                if two[row][i].action == 0 and two[row][i].timer != 0:
                    two[row][i].action = 1
                    two[row][i].timer -= 1
                else:
                    two[two[row][i].seat][i] = 1
                    seated.append(two[row][i])
                    sit += 1
                    two[row][i] = 0
    return two, sit, seated

def reset_action(two):
    for i in range(1, 41):
        if two[2][i] != 0:
            two[2][i].action = 0
            two[2][i].board+=1
        if two[6][i] != 0:
            two[6][i].action = 0
            two[6][i].board += 1
    for i in range(7):
        if two[i][0] != 0:
            two[i][0].action = 0
            two[i][0].board += 1
        if two[i][41] != 0:
            two[i][41].action = 0
            two[i][41].board += 1
    return two

def plot_fig(two, viewer):
    for i in range(9):
        for j in range(42):
            if two[i][j] != 0:
                if two[i][j] == 1:
                    viewer[i][j] = 4
                else:
                    #if two[i][j].speed == 49:
                        #viewer[i][j] = 8
                    #else:
                    viewer[i][j] = 10
            else:
                if i == 2 or i == 6:
                    viewer[i][j] = 0
                else:
                    viewer[i][j] = 2
    plt.close()
    fig, ax = plt.subplots()
    im = ax.imshow(viewer)
    plt.draw()
    plt.pause(0.0000001)


def run_two(two, p_list_1, p_list_2):
    sit = 0
    time = 0
    seated = []
    viewer =  [[0] * 42 for _ in range(9)]
    while sit < 246:
        time += 1
        if two[0][0] == 0 and len(p_list_1) != 0:
            two[0][0] = p_list_1.pop()
            two[0][0].action = 1
        for i in range(2):
            two = next_row(two, i, 0)
        two = check_intersect(two, 2, 0, 1)
        two, sit, seated = check_left(two, 2, sit, seated)
        for i in range(3, 6):
            two = next_row(two, i, 0)
        two = check_intersect_2(two, 6, 0, 1)
        two, sit, seated = check_left(two, 6, sit, seated)
        if two[0][41] == 0 and len(p_list_2) != 0:
            two[0][41] = p_list_2.pop()
            two[0][41].action = 1
        for i in range(2):
            two = next_row(two, i, 41)
        two = check_intersect(two, 2, 41, -1)
        two, sit, seated = check_right(two, 2, sit, seated)
        for i in range(3, 6):
            two = next_row(two, i, 41)
        two = check_intersect_2(two, 6, 41, -1)
        two, sit, seated = check_right(two, 6, sit, seated)
        two = reset_action(two)
        #plot_fig(two, viewer)
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
for i in range(1000):
    print(i)
    p_list_1 = []
    p_list_2 = []
    p_list_1, p_list_2 = create_passenger_list()
    p_list_1, p_list_2 = initialize_passenger_list(p_list_1, p_list_2)
    two = [[0] * 42 for _ in range(11)]
    two = initialize_array(two)
    a, b, c, d, e = run_two(two, p_list_1, p_list_2)
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
#np.save('in_two_time.npy', np_time)
#np.save('in_two_board_avg.npy', np_board_avg)
#np.save('in_two_wait_avg.npy', np_wait_avg)
#np.save('in_two_bag_avg.npy', np_bag_avg)
#np.save('in_two_stop_avg.npy', np_stop_avg)
